CREATE OR REPLACE PROCEDURE p_create_customer (
    p_full_name IN VARCHAR2, p_email IN VARCHAR2, p_phone IN VARCHAR2,
    p_address IN VARCHAR2, p_customer_id OUT NUMBER
) AS
BEGIN
    IF TRIM(p_full_name) IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'Customer name is required.');
    END IF;
    INSERT INTO customers(full_name,email,phone,address)
    VALUES (TRIM(p_full_name),NULLIF(TRIM(p_email),''),NULLIF(TRIM(p_phone),''),NULLIF(TRIM(p_address),''))
    RETURNING customer_id INTO p_customer_id;
    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE p_open_account (
    p_customer_id IN NUMBER, p_account_type IN VARCHAR2,
    p_initial_deposit IN NUMBER, p_account_id OUT NUMBER
) AS
    v_count NUMBER;
    v_type VARCHAR2(10) := UPPER(TRIM(p_account_type));
BEGIN
    IF p_initial_deposit IS NULL OR p_initial_deposit < 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Initial deposit cannot be negative.');
    END IF;
    IF v_type NOT IN ('SAVINGS','CURRENT') THEN
        RAISE_APPLICATION_ERROR(-20003, 'Account type must be SAVINGS or CURRENT.');
    END IF;
    SELECT COUNT(*) INTO v_count FROM customers WHERE customer_id=p_customer_id;
    IF v_count=0 THEN RAISE_APPLICATION_ERROR(-20004, 'Customer does not exist.'); END IF;
    INSERT INTO accounts(customer_id,account_type,balance)
    VALUES (p_customer_id,v_type,p_initial_deposit) RETURNING account_id INTO p_account_id;
    IF p_initial_deposit > 0 THEN
        INSERT INTO transactions(transaction_type,amount,to_account_id,note)
        VALUES ('OPENING',p_initial_deposit,p_account_id,'Initial account deposit');
    END IF;
    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE p_deposit (
    p_account_id IN NUMBER, p_amount IN NUMBER, p_note IN VARCHAR2 DEFAULT NULL
) AS
    v_status accounts.status%TYPE;
BEGIN
    IF p_amount IS NULL OR p_amount<=0 THEN
        RAISE_APPLICATION_ERROR(-20005, 'Deposit amount must be greater than zero.');
    END IF;
    SELECT status INTO v_status FROM accounts WHERE account_id=p_account_id FOR UPDATE;
    IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20006, 'Account is not active.'); END IF;
    UPDATE accounts SET balance=balance+p_amount WHERE account_id=p_account_id;
    INSERT INTO transactions(transaction_type,amount,to_account_id,note)
    VALUES ('DEPOSIT',p_amount,p_account_id,p_note);
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20007, 'Account not found.');
    WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/

CREATE OR REPLACE PROCEDURE p_withdraw (
    p_account_id IN NUMBER, p_amount IN NUMBER, p_note IN VARCHAR2 DEFAULT NULL
) AS
    v_balance accounts.balance%TYPE;
    v_status accounts.status%TYPE;
BEGIN
    IF p_amount IS NULL OR p_amount<=0 THEN
        RAISE_APPLICATION_ERROR(-20008, 'Withdrawal amount must be greater than zero.');
    END IF;
    SELECT balance,status INTO v_balance,v_status FROM accounts
    WHERE account_id=p_account_id FOR UPDATE;
    IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20009, 'Account is not active.'); END IF;
    IF v_balance<p_amount THEN RAISE_APPLICATION_ERROR(-20010, 'Insufficient balance.'); END IF;
    UPDATE accounts SET balance=balance-p_amount WHERE account_id=p_account_id;
    INSERT INTO transactions(transaction_type,amount,from_account_id,note)
    VALUES ('WITHDRAW',p_amount,p_account_id,p_note);
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20011, 'Account not found.');
    WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/

CREATE OR REPLACE PROCEDURE p_transfer (
    p_from_account_id IN NUMBER, p_to_account_id IN NUMBER,
    p_amount IN NUMBER, p_note IN VARCHAR2 DEFAULT NULL
) AS
    v_balance accounts.balance%TYPE;
    v_from_status accounts.status%TYPE;
    v_to_status accounts.status%TYPE;
BEGIN
    IF p_from_account_id=p_to_account_id THEN
        RAISE_APPLICATION_ERROR(-20012, 'Source and destination accounts must differ.');
    END IF;
    IF p_amount IS NULL OR p_amount<=0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'Transfer amount must be greater than zero.');
    END IF;
    SELECT balance,status INTO v_balance,v_from_status FROM accounts
    WHERE account_id=p_from_account_id FOR UPDATE;
    SELECT status INTO v_to_status FROM accounts
    WHERE account_id=p_to_account_id FOR UPDATE;
    IF v_from_status<>'ACTIVE' OR v_to_status<>'ACTIVE' THEN
        RAISE_APPLICATION_ERROR(-20014, 'Both accounts must be active.');
    END IF;
    IF v_balance<p_amount THEN RAISE_APPLICATION_ERROR(-20015, 'Insufficient balance for transfer.'); END IF;
    UPDATE accounts SET balance=balance-p_amount WHERE account_id=p_from_account_id;
    UPDATE accounts SET balance=balance+p_amount WHERE account_id=p_to_account_id;
    INSERT INTO transactions(transaction_type,amount,from_account_id,to_account_id,note)
    VALUES ('TRANSFER_OUT',p_amount,p_from_account_id,p_to_account_id,p_note);
    INSERT INTO transactions(transaction_type,amount,from_account_id,to_account_id,note)
    VALUES ('TRANSFER_IN',p_amount,p_from_account_id,p_to_account_id,p_note);
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20016, 'Source or destination account not found.');
    WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/

CREATE OR REPLACE PROCEDURE p_close_account(p_account_id IN NUMBER) AS
    v_balance NUMBER(14,2);
BEGIN
    SELECT balance INTO v_balance FROM accounts WHERE account_id=p_account_id FOR UPDATE;
    IF v_balance<>0 THEN RAISE_APPLICATION_ERROR(-20017, 'Account balance must be zero before closing.'); END IF;
    UPDATE accounts SET status='CLOSED' WHERE account_id=p_account_id;
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20018, 'Account not found.');
    WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
