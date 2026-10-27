import os, sys, tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from contextlib import closing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import get_connection, query_all, call_procedure

BG="#0A1020"; SIDE="#0E1729"; PANEL="#121E32"; PANEL2="#17263D"; BORDER="#263650"
TEXT="#EAF1FC"; MUTED="#91A4BF"; TEAL="#2DD4BF"; TEAL_DARK="#0F766E"; RED="#FB7185"; GREEN="#86EFAC"
FONT="Segoe UI"

class BankEaseApp(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("BankEase | Banking Management System")
        self.geometry("1360x820"); self.minsize(1120,700); self.configure(bg=BG)
        self.current_page=None; self.page_frames={}; self.nav_buttons={}; self._style(); self._layout()
        self.show_page("Dashboard"); self.refresh_all()
    def _style(self):
        s=ttk.Style(self)
        try:s.theme_use("clam")
        except tk.TclError:pass
        s.configure("TFrame",background=BG); s.configure("Panel.TFrame",background=PANEL)
        s.configure("TLabel",background=BG,foreground=TEXT,font=(FONT,10))
        s.configure("Muted.TLabel",background=BG,foreground=MUTED,font=(FONT,10))
        s.configure("PageTitle.TLabel",background=BG,foreground=TEXT,font=(FONT,25,"bold"))
        s.configure("Sub.TLabel",background=BG,foreground=MUTED,font=(FONT,10))
        s.configure("TEntry",fieldbackground="#0B1425",foreground=TEXT,insertcolor=TEXT,bordercolor=BORDER,lightcolor=BORDER,darkcolor=BORDER,padding=9)
        s.configure("TCombobox",fieldbackground="#0B1425",background=PANEL2,foreground=TEXT,arrowcolor=TEAL,padding=8)
        s.map("TCombobox",fieldbackground=[("readonly","#0B1425")],foreground=[("readonly",TEXT)])
        s.configure("Treeview",background="#0F1A2D",fieldbackground="#0F1A2D",foreground=TEXT,rowheight=32,borderwidth=0,font=(FONT,9))
        s.configure("Treeview.Heading",background=PANEL2,foreground=TEAL,font=(FONT,9,"bold"),relief="flat",padding=9)
        s.map("Treeview",background=[("selected","#115E59")],foreground=[("selected","#FFFFFF")])
        s.configure("TScrollbar",background=PANEL2,troughcolor=BG,bordercolor=BG,arrowcolor=TEXT)
    def _layout(self):
        top=tk.Frame(self,bg=SIDE,height=78);top.pack(fill="x");top.pack_propagate(False)
        tk.Label(top,text="◆  BankEase",bg=SIDE,fg=TEAL,font=(FONT,23,"bold")).pack(side="left",padx=25)
        tk.Label(top,text="BANKING MANAGEMENT  /  ORACLE PL/SQL",bg=SIDE,fg=MUTED,font=(FONT,10,"bold")).pack(side="left",padx=14)
        tk.Label(top,text="●  LOCAL DATABASE",bg=SIDE,fg=GREEN,font=(FONT,9,"bold")).pack(side="right",padx=25)
        body=tk.Frame(self,bg=BG);body.pack(fill="both",expand=True)
        self.sidebar=tk.Frame(body,bg=SIDE,width=218);self.sidebar.pack(side="left",fill="y");self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text="WORKSPACE",bg=SIDE,fg="#647995",font=(FONT,9,"bold")).pack(anchor="w",padx=22,pady=(28,12))
        for title,icon in [("Dashboard","▦"),("Customers","♙"),("Accounts","▣"),("Operations","⇄"),("Transactions","≡")]:
            b=tk.Button(self.sidebar,text=f"  {icon}    {title}",command=lambda t=title:self.show_page(t),anchor="w",bd=0,relief="flat",cursor="hand2",font=(FONT,11,"bold"),padx=14,pady=13,bg=SIDE,fg=MUTED,activebackground=PANEL2,activeforeground=TEAL)
            b.pack(fill="x",padx=12,pady=3);self.nav_buttons[title]=b
        tk.Frame(self.sidebar,bg=BORDER,height=1).pack(fill="x",padx=20,pady=24)
        tk.Label(self.sidebar,text="BANKING DEMO",bg=SIDE,fg=TEAL,font=(FONT,9,"bold")).pack(anchor="w",padx=22)
        tk.Label(self.sidebar, text="Python  •  Tkinter\nOracle XE  •  PL/SQL", bg=SIDE, fg=MUTED, justify="left", font=(FONT, 9)).pack(anchor="w", padx=22, pady=8)
        self.content=tk.Frame(body,bg=BG);self.content.pack(side="left",fill="both",expand=True,padx=28,pady=24)
        self._build_dashboard();self._build_customers();self._build_accounts();self._build_operations();self._build_transactions()
        bottom=tk.Frame(self,bg=SIDE,height=28);bottom.pack(fill="x",side="bottom");bottom.pack_propagate(False)
        self.status=tk.StringVar(value="Ready • Connected to local Oracle service XEPDB1")
        tk.Label(bottom,textvariable=self.status,bg=SIDE,fg=MUTED,font=(FONT,9)).pack(side="left",padx=18,pady=5)
        tk.Label(bottom,text="ACADEMIC PROJECT • DEMO DATA ONLY",bg=SIDE,fg="#647995",font=(FONT,8,"bold")).pack(side="right",padx=18)
    def _page(self,name,title,subtitle):
        f=tk.Frame(self.content,bg=BG);self.page_frames[name]=f
        tk.Label(f,text=title,bg=BG,fg=TEXT,font=(FONT,25,"bold")).pack(anchor="w")
        tk.Label(f,text=subtitle,bg=BG,fg=MUTED,font=(FONT,10)).pack(anchor="w",pady=(5,20))
        return f
    def show_page(self,name):
        for f in self.page_frames.values():f.pack_forget()
        self.page_frames[name].pack(fill="both",expand=True);self.current_page=name
        for n,b in self.nav_buttons.items():b.configure(bg=("#15364A" if n==name else SIDE),fg=(TEAL if n==name else MUTED))
        self.status.set(f"{name} • BankEase workspace")
    def _button(self,parent,text,cmd,primary=True):
        return tk.Button(parent,text=text,command=cmd,bg=(TEAL_DARK if primary else PANEL2),fg=("#ECFEFF" if primary else TEXT),activebackground=TEAL,activeforeground="#06131B",bd=0,cursor="hand2",font=(FONT,9,"bold"),padx=15,pady=9)
    def _card(self,parent,title,value,key,accent=TEAL):
        box=tk.Frame(parent,bg=PANEL,highlightbackground=BORDER,highlightthickness=1);box.pack(side="left",fill="both",expand=True,padx=(0,12))
        tk.Label(box,text=title.upper(),bg=PANEL,fg=MUTED,font=(FONT,9,"bold")).pack(anchor="w",padx=17,pady=(16,5))
        v=tk.StringVar(value=value);self.card_vars[key]=v
        tk.Label(box,textvariable=v,bg=PANEL,fg=accent,font=(FONT,22,"bold")).pack(anchor="w",padx=17,pady=(0,15))
    def _tree(self,parent,cols,heads,widths=None,height=10):
        wrap=tk.Frame(parent,bg=PANEL);wrap.pack(fill="both",expand=True,pady=(10,0))
        tree=ttk.Treeview(wrap,columns=cols,show="headings",height=height)
        ys=ttk.Scrollbar(wrap,orient="vertical",command=tree.yview);xs=ttk.Scrollbar(wrap,orient="horizontal",command=tree.xview)
        tree.configure(yscrollcommand=ys.set,xscrollcommand=xs.set);tree.grid(row=0,column=0,sticky="nsew");ys.grid(row=0,column=1,sticky="ns");xs.grid(row=1,column=0,sticky="ew")
        wrap.rowconfigure(0,weight=1);wrap.columnconfigure(0,weight=1)
        for i,(c,h) in enumerate(zip(cols,heads)):tree.heading(c,text=h);tree.column(c,width=(widths[i] if widths else 130),anchor="w",stretch=True)
        return tree
    def _build_dashboard(self):
        f=self._page("Dashboard","Good evening, welcome back.","Here is the latest overview of your BankEase demo environment.")
        self.card_vars={};cards=tk.Frame(f,bg=BG);cards.pack(fill="x",pady=(0,22))
        for x in [("Customers","—","customers",TEAL),("Accounts","—","accounts","#A5B4FC"),("Active balance (₹)","—","balance",GREEN),("Transactions","—","transactions","#FBBF24")]:self._card(cards,*x)
        row=tk.Frame(f,bg=BG);row.pack(fill="both",expand=True)
        left=tk.Frame(row,bg=BG);left.pack(fill="both",expand=True)
        tk.Label(left,text="Recent activity",bg=BG,fg=TEXT,font=(FONT,16,"bold")).pack(anchor="w")
        tk.Label(left,text="Latest recorded account events",bg=BG,fg=MUTED,font=(FONT,9)).pack(anchor="w",pady=(3,5))
        self.recent_tree=self._tree(left,("id","type","amount","from","to","date"),("Txn ID","Type","Amount (₹)","From","To","Date"),(70,120,120,75,75,145),9)
        side=tk.Frame(row,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,width=210);side.pack(side="right",fill="y",padx=(18,0));side.pack_propagate(False)
        tk.Label(side,text="QUICK ACTIONS",bg=PANEL,fg=TEAL,font=(FONT,10,"bold")).pack(anchor="w",padx=16,pady=(18,14))
        for label,page in [("＋  Register customer","Customers"),("▣  View accounts","Accounts"),("⇄  Banking operations","Operations"),("≡  Transaction history","Transactions")]:
            tk.Button(side,text=label,command=lambda p=page:self.show_page(p),bg=PANEL2,fg=TEXT,activebackground=TEAL_DARK,activeforeground="white",bd=0,anchor="w",font=(FONT,9,"bold"),padx=12,pady=12,cursor="hand2").pack(fill="x",padx=12,pady=5)
        tk.Label(side,text="Security reminder",bg=PANEL,fg="#FBBF24",font=(FONT,9,"bold")).pack(anchor="w",padx=16,pady=(24,5))
        tk.Label(side,text="Educational demo only.\nDo not use real customer\nor financial information.",bg=PANEL,fg=MUTED,justify="left",font=(FONT,9)).pack(anchor="w",padx=16)
    def _entry(self,parent,label,row,col,width=24):
        tk.Label(parent,text=label,bg=PANEL,fg=MUTED,font=(FONT,9,"bold")).grid(row=row,column=col,sticky="w",padx=8,pady=(8,4))
        e=ttk.Entry(parent,width=width);e.grid(row=row+1,column=col,sticky="ew",padx=8,pady=(0,8));return e
    def _formbox(self,parent,title):
        box=tk.Frame(parent,bg=PANEL,highlightbackground=BORDER,highlightthickness=1);box.pack(fill="x",pady=(0,14));tk.Label(box,text=title,bg=PANEL,fg=TEXT,font=(FONT,12,"bold")).grid(row=0,column=0,columnspan=4,sticky="w",padx=14,pady=(12,2));return box
    def _build_customers(self):
        f=self._page("Customers","Customer directory","Register customers and review saved customer records.")
        form=self._formbox(f,"New customer")
        self.c_name=self._entry(form,"FULL NAME *",1,0);self.c_email=self._entry(form,"EMAIL",1,1);self.c_phone=self._entry(form,"PHONE",1,2);self.c_address=self._entry(form,"ADDRESS",1,3,32)
        self._button(form,"＋  Add customer",self.add_customer).grid(row=1,column=4,rowspan=2,padx=12,pady=15,sticky="ns")
        bar=tk.Frame(f,bg=BG);bar.pack(fill="x");tk.Label(bar,text="Registered customers",bg=BG,fg=TEXT,font=(FONT,14,"bold")).pack(side="left");self._button(bar,"↻ Refresh",self.refresh_customers,False).pack(side="right")
        self.customer_tree=self._tree(f,("id","name","email","phone","address","created"),("Customer ID","Full name","Email","Phone","Address","Created"),(80,170,190,120,240,150),12)
    def _build_accounts(self):
        f=self._page("Accounts","Account portfolio","Browse account balances, types and current status.")
        bar=tk.Frame(f,bg=BG);bar.pack(fill="x");tk.Label(bar,text="All accounts",bg=BG,fg=TEXT,font=(FONT,14,"bold")).pack(side="left");self._button(bar,"↻ Refresh accounts",self.refresh_accounts,False).pack(side="right")
        self.account_tree=self._tree(f,("id","cid","name","type","balance","status","opened"),("Account ID","Customer ID","Customer","Account type","Balance (₹)","Status","Opened"),(85,90,190,120,130,100,155),15)
        tk.Label(f,text="Tip: use the Operations page to open an account, deposit, withdraw or transfer funds.",bg=BG,fg=MUTED,font=(FONT,9)).pack(anchor="w",pady=10)
    def _build_operations(self):
        f=self._page("Operations","Banking operations","Actions are executed through Oracle PL/SQL procedures.")
        # Open account
        b=self._formbox(f,"01  Open a new account")
        self.open_customer=self._entry(b,"CUSTOMER ID *",1,0);tk.Label(b,text="ACCOUNT TYPE",bg=PANEL,fg=MUTED,font=(FONT,9,"bold")).grid(row=1,column=1,sticky="w",padx=8,pady=(8,4))
        self.open_type=ttk.Combobox(b,values=["SAVINGS","CURRENT"],state="readonly",width=20);self.open_type.current(0);self.open_type.grid(row=2,column=1,sticky="ew",padx=8,pady=(0,8))
        self.open_amount=self._entry(b,"INITIAL DEPOSIT (₹)",1,2);self._button(b,"Open account",self.open_account).grid(row=1,column=3,rowspan=2,padx=12,pady=12,sticky="ns")
        b2=self._formbox(f,"02  Deposit or withdraw")
        self.money_account=self._entry(b2,"ACCOUNT ID *",1,0);self.money_amount=self._entry(b2,"AMOUNT (₹) *",1,1);self.money_note=self._entry(b2,"NOTE / DESCRIPTION",1,2,30)
        actions=tk.Frame(b2,bg=PANEL);actions.grid(row=1,column=3,rowspan=2,padx=12,pady=12,sticky="ns")
        self._button(actions,"＋  Deposit",lambda:self.money_operation("deposit")).pack(fill="x",pady=(0,7));self._button(actions,"−  Withdraw",lambda:self.money_operation("withdraw"),False).pack(fill="x")
        b3=self._formbox(f,"03  Transfer between accounts")
        self.from_id=self._entry(b3,"FROM ACCOUNT ID *",1,0);self.to_id=self._entry(b3,"TO ACCOUNT ID *",1,1);self.transfer_amount=self._entry(b3,"AMOUNT (₹) *",1,2);self.transfer_note=self._entry(b3,"NOTE",1,3)
        self._button(b3,"⇄  Transfer funds",self.transfer).grid(row=1,column=4,rowspan=2,padx=12,pady=12,sticky="ns")
        tk.Label(f,text="Controls: positive amounts, sufficient balance, active accounts and distinct transfer accounts are checked in PL/SQL.",bg=BG,fg=MUTED,font=(FONT,9),wraplength=900,justify="left").pack(anchor="w",pady=4)
    def _build_transactions(self):
        f=self._page("Transactions","Transaction ledger","Review recent deposits, withdrawals, opening entries and transfers.")
        bar=tk.Frame(f,bg=BG);bar.pack(fill="x");tk.Label(bar,text="Latest transactions",bg=BG,fg=TEXT,font=(FONT,14,"bold")).pack(side="left");self._button(bar,"↻ Refresh history",self.refresh_transactions,False).pack(side="right")
        self.txn_tree=self._tree(f,("id","type","amount","from","to","note","date"),("Txn ID","Type","Amount (₹)","From account","To account","Description","Created"),(75,125,120,100,100,230,155),15)
    @staticmethod
    def money(text,label,zero=False):
        try:n=Decimal(text.strip())
        except (InvalidOperation,AttributeError):raise ValueError(f"{label} must be a valid number.")
        if not n.is_finite() or n<0 or (n==0 and not zero):raise ValueError(f"{label} must be {'zero or greater' if zero else 'greater than zero'}.")
        if n.as_tuple().exponent < -2:raise ValueError(f"{label} can have at most two decimal places.")
        return n
    @staticmethod
    def integer(text,label):
        try:n=int(text.strip())
        except (ValueError,AttributeError):raise ValueError(f"{label} must be a whole number.")
        if n<=0:raise ValueError(f"{label} must be positive.")
        return n
    def action(self,fn):
        try:fn();self.refresh_all()
        except Exception as e:messagebox.showerror("Operation failed",str(e),parent=self);self.status.set("Operation failed • check the message")
    def add_customer(self):
        def run():
            name=self.c_name.get().strip()
            if not name:raise ValueError("Full name is required.")
            with closing(get_connection()) as conn:
                with conn.cursor() as cur:
                    out=cur.var(int);cur.callproc("p_create_customer",[name,self.c_email.get().strip() or None,self.c_phone.get().strip() or None,self.c_address.get().strip() or None,out]);cid=out.getvalue()
            messagebox.showinfo("Customer created",f"Customer ID: {cid}",parent=self)
            for e in (self.c_name,self.c_email,self.c_phone,self.c_address):e.delete(0,"end")
        self.action(run)
    def open_account(self):
        def run():
            cid=self.integer(self.open_customer.get(),"Customer ID");amt=self.money(self.open_amount.get() or "0","Initial deposit",True)
            with closing(get_connection()) as conn:
                with conn.cursor() as cur:out=cur.var(int);cur.callproc("p_open_account",[cid,self.open_type.get(),amt,out]);aid=out.getvalue()
            messagebox.showinfo("Account opened",f"Account ID: {aid}",parent=self)
            self.open_customer.delete(0,"end");self.open_amount.delete(0,"end")
        self.action(run)
    def money_operation(self,kind):
        def run():
            aid=self.integer(self.money_account.get(),"Account ID");amt=self.money(self.money_amount.get(),"Amount");proc="p_deposit" if kind=="deposit" else "p_withdraw"
            call_procedure(proc,[aid,amt,self.money_note.get().strip() or None]);messagebox.showinfo("Success",f"{kind.title()} completed.",parent=self)
            self.money_amount.delete(0,"end");self.money_note.delete(0,"end")
        self.action(run)
    def transfer(self):
        def run():
            src=self.integer(self.from_id.get(),"Source account ID");dst=self.integer(self.to_id.get(),"Destination account ID");amt=self.money(self.transfer_amount.get(),"Amount")
            call_procedure("p_transfer",[src,dst,amt,self.transfer_note.get().strip() or None]);messagebox.showinfo("Transfer complete","Funds transferred successfully.",parent=self)
            for e in (self.from_id,self.to_id,self.transfer_amount,self.transfer_note):e.delete(0,"end")
        self.action(run)
    @staticmethod
    def _fill(tree,rows):
        tree.delete(*tree.get_children())
        for row in rows:tree.insert("","end",values=tuple("" if x is None else str(x) for x in row))
    def refresh_customers(self):self._fill(self.customer_tree,query_all("SELECT customer_id,full_name,email,phone,address,TO_CHAR(created_at,'YYYY-MM-DD HH24:MI') FROM customers ORDER BY customer_id DESC"))
    def refresh_accounts(self):self._fill(self.account_tree,query_all("SELECT account_id,customer_id,full_name,account_type,TO_CHAR(balance,'FM9999999990.00'),status,TO_CHAR(opened_at,'YYYY-MM-DD HH24:MI') FROM v_account_summary ORDER BY account_id DESC"))
    def refresh_transactions(self):self._fill(self.txn_tree,query_all("SELECT transaction_id,transaction_type,TO_CHAR(amount,'FM9999999990.00'),from_account_id,to_account_id,note,TO_CHAR(created_at,'YYYY-MM-DD HH24:MI') FROM v_transaction_history ORDER BY transaction_id DESC FETCH FIRST 250 ROWS ONLY"))
    def refresh_dashboard(self):
        r=query_all("SELECT (SELECT COUNT(*) FROM customers),(SELECT COUNT(*) FROM accounts),(SELECT NVL(SUM(balance),0) FROM accounts WHERE status='ACTIVE'),(SELECT COUNT(*) FROM transactions) FROM dual")[0]
        self.card_vars['customers'].set(f"{r[0]:,}");self.card_vars['accounts'].set(f"{r[1]:,}");self.card_vars['balance'].set(f"₹ {r[2]:,.2f}");self.card_vars['transactions'].set(f"{r[3]:,}")
        rows=query_all("SELECT transaction_id,transaction_type,TO_CHAR(amount,'FM9999999990.00'),from_account_id,to_account_id,TO_CHAR(created_at,'YYYY-MM-DD HH24:MI') FROM transactions ORDER BY transaction_id DESC FETCH FIRST 10 ROWS ONLY")
        self._fill(self.recent_tree,rows)
    def refresh_all(self):
        try:self.refresh_dashboard();self.refresh_customers();self.refresh_accounts();self.refresh_transactions();self.status.set("Connected • Oracle XEPDB1 • Data refreshed")
        except Exception as e:
            self.status.set("Database connection needs attention")
            messagebox.showerror("Database connection", "Could not load BankEase.\n\nCheck Oracle is running, run the SQL scripts in order, and verify app/db_config.py.\n\nDetails:\n"+str(e),parent=self)

if __name__=="__main__":
    try:BankEaseApp().mainloop()
    except Exception as exc:messagebox.showerror("BankEase startup error",str(exc))
