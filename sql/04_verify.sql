SELECT * FROM customers ORDER BY customer_id;
SELECT * FROM v_account_summary ORDER BY account_id;
SELECT * FROM v_transaction_history ORDER BY transaction_id DESC FETCH FIRST 20 ROWS ONLY;
SELECT object_name, object_type, status FROM user_objects
WHERE object_type IN ('PROCEDURE','VIEW') ORDER BY object_type,object_name;
SELECT name, type, line, position, text FROM user_errors ORDER BY name, sequence;
