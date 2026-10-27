-- Run once as BANK_USER after 01_schema.sql and 02_plsql_programs.sql.
-- This creates fictional demo records. Do not rerun unless schema has been reset.
DECLARE v_c1 NUMBER; v_c2 NUMBER; v_a1 NUMBER; v_a2 NUMBER;
BEGIN
  p_create_customer('Aanya Sharma','aanya.demo@example.com','9000000001','Demo address, India',v_c1);
  p_create_customer('Rohan Verma','rohan.demo@example.com','9000000002','Demo address, India',v_c2);
  p_open_account(v_c1,'SAVINGS',12500,v_a1);
  p_open_account(v_c2,'CURRENT',8000,v_a2);
END;
/
