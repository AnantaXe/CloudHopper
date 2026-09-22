CREATE SCHEMA IF NOT EXISTS source_db;

SET search_path TO source_db, public;

CREATE TABLE IF NOT EXISTS source_db.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_db.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES source_db.customers(customer_id) ON DELETE RESTRICT,
    order_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled')),
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_db.order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES source_db.orders(order_id) ON DELETE CASCADE,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    line_total NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_db.payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES source_db.orders(order_id) ON DELETE CASCADE,
    payment_method VARCHAR(30) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_db.audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(60) NOT NULL,
    record_id BIGINT NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION source_db.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION source_db.log_audit_changes()
RETURNS TRIGGER AS $$
DECLARE
    v_record_id BIGINT;
BEGIN
    IF TG_TABLE_NAME = 'orders' THEN
        v_record_id := COALESCE(NEW.order_id, OLD.order_id);
    ELSIF TG_TABLE_NAME = 'payments' THEN
        v_record_id := COALESCE(NEW.payment_id, OLD.payment_id);
    ELSE
        v_record_id := COALESCE(NEW.id, OLD.id);
    END IF;

    IF (TG_OP = 'INSERT') THEN
        INSERT INTO source_db.audit_log(table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, v_record_id, TG_OP, to_jsonb(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO source_db.audit_log(table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, v_record_id, TG_OP, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO source_db.audit_log(table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, v_record_id, TG_OP, to_jsonb(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION source_db.get_customer_order_total(p_customer_id INT)
RETURNS NUMERIC(12,2)
LANGUAGE sql
AS $$
    SELECT COALESCE(SUM(total_amount), 0)
    FROM source_db.orders
    WHERE customer_id = p_customer_id;
$$;

CREATE OR REPLACE FUNCTION source_db.calculate_order_total(p_order_id INT)
RETURNS NUMERIC(12,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(12,2);
BEGIN
    SELECT COALESCE(SUM(quantity * unit_price), 0)
    INTO v_total
    FROM source_db.order_items
    WHERE order_id = p_order_id;

    RETURN v_total;
END;
$$;

CREATE OR REPLACE PROCEDURE source_db.create_order(
    p_customer_id INT,
    p_product_name VARCHAR(100),
    p_quantity INT,
    p_unit_price NUMERIC(10,2),
    p_status VARCHAR(20) DEFAULT 'pending'
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INT;
BEGIN
    INSERT INTO source_db.orders (customer_id, status, total_amount)
    VALUES (p_customer_id, p_status, 0)
    RETURNING order_id INTO v_order_id;

    INSERT INTO source_db.order_items (order_id, product_name, quantity, unit_price)
    VALUES (v_order_id, p_product_name, p_quantity, p_unit_price);

    UPDATE source_db.orders
    SET total_amount = source_db.calculate_order_total(v_order_id),
        updated_at = NOW()
    WHERE order_id = v_order_id;
END;
$$;

CREATE OR REPLACE PROCEDURE source_db.mark_order_paid(p_order_id INT, p_payment_method VARCHAR(30), p_amount NUMERIC(12,2))
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO source_db.payments (order_id, payment_method, payment_status, amount, paid_at)
    VALUES (p_order_id, p_payment_method, 'completed', p_amount, NOW());

    UPDATE source_db.orders
    SET status = 'paid',
        updated_at = NOW()
    WHERE order_id = p_order_id;
END;
$$;

CREATE OR REPLACE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON source_db.customers
FOR EACH ROW
EXECUTE FUNCTION source_db.set_updated_at();

CREATE OR REPLACE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON source_db.orders
FOR EACH ROW
EXECUTE FUNCTION source_db.set_updated_at();

CREATE OR REPLACE TRIGGER trg_orders_audit_log
AFTER INSERT OR UPDATE OF status, total_amount OR DELETE ON source_db.orders
FOR EACH ROW
EXECUTE FUNCTION source_db.log_audit_changes();

CREATE OR REPLACE TRIGGER trg_payments_audit_log
AFTER INSERT OR UPDATE OF payment_status, amount OR DELETE ON source_db.payments
FOR EACH ROW
EXECUTE FUNCTION source_db.log_audit_changes();

CREATE INDEX IF NOT EXISTS idx_customers_email
    ON source_db.customers (email);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id
    ON source_db.orders (customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_status
    ON source_db.orders (status);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id
    ON source_db.order_items (order_id);

CREATE INDEX IF NOT EXISTS idx_payments_order_id
    ON source_db.payments (order_id);

CREATE INDEX IF NOT EXISTS idx_payments_status
    ON source_db.payments (payment_status);

CREATE VIEW source_db.customer_order_summary AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spend,
    COALESCE(MAX(o.order_date), NULL) AS last_order_date
FROM source_db.customers c
LEFT JOIN source_db.orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

CREATE VIEW source_db.order_detail_summary AS
SELECT
    o.order_id,
    o.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    o.status,
    o.total_amount,
    COUNT(oi.item_id) AS item_count,
    SUM(oi.quantity) AS total_quantity
FROM source_db.orders o
JOIN source_db.customers c ON c.customer_id = o.customer_id
LEFT JOIN source_db.order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.customer_id, c.first_name, c.last_name, o.status, o.total_amount;

INSERT INTO source_db.customers (first_name, last_name, email)
VALUES
    ('Alice', 'Johnson', 'alice.johnson@example.com'),
    ('Bob', 'Smith', 'bob.smith@example.com'),
    ('Carol', 'Davis', 'carol.davis@example.com')
ON CONFLICT (email) DO NOTHING;

INSERT INTO source_db.orders (customer_id, status, total_amount)
VALUES
    (1, 'pending', 0.00),
    (2, 'paid', 0.00),
    (3, 'shipped', 0.00)
ON CONFLICT DO NOTHING;

INSERT INTO source_db.order_items (order_id, product_name, quantity, unit_price)
VALUES
    (1, 'Laptop', 1, 999.99),
    (1, 'Mouse', 2, 24.99),
    (2, 'Keyboard', 1, 79.50),
    (3, 'Monitor', 1, 249.00)
ON CONFLICT DO NOTHING;

UPDATE source_db.orders
SET total_amount = source_db.calculate_order_total(order_id)
WHERE order_id IN (1, 2, 3);

INSERT INTO source_db.payments (order_id, payment_method, payment_status, amount, paid_at)
VALUES
    (2, 'credit_card', 'completed', 79.50, NOW()),
    (3, 'bank_transfer', 'completed', 249.00, NOW())
ON CONFLICT DO NOTHING;

ALTER TABLE source_db.orders
    ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES source_db.customers(customer_id);

ALTER TABLE source_db.order_items
    ADD CONSTRAINT fk_order_items_orders
    FOREIGN KEY (order_id) REFERENCES source_db.orders(order_id);

ALTER TABLE source_db.payments
    ADD CONSTRAINT fk_payments_order
    FOREIGN KEY (order_id) REFERENCES source_db.orders(order_id);
