import matplotlib.pyplot as plt
from db_connection import *
from tkinter import *
from tkinter import messagebox

#   GUI View/Controller Class
#   Windows, graphs, infoboxes, database scroller
#   Works in concert with db_connection.py and loan.py
class MainWindow(Frame):

    def __init__(self, master=Tk(), connection=None):
        Frame.__init__(self, master)
        self.master = master
        self.my_loan = StandardLoan(0, 0, 0)
        self.loan_memory = []
        self.my_connection = connection
        self.init_window()

    def start(self):
        self.mainloop()

    ####################
    #   VIEW
    ####################
    def init_window(self):
        self.master.geometry("600x400")
        self.master.title("Loan Amortization Calculator")

        self.create_labels()
        self.create_entries()
        self.create_buttons()

    #   Create and format labels in window
    def create_labels(self):
        loan_title = Label(self.master, text="Loan title: ")
        bal_label = Label(self.master, text="Starting balance: ")
        int_label = Label(self.master, text="Interest rate: ")
        pymt_label = Label(self.master, text="Monthly payment amount: ")
        num = Label(self.master, text="Number of payments:")
        new_amt = Label(self.master, text="New payment amount:")

        #   Format Labels
        loan_title.grid(row=1, column=0, sticky=W, padx=5)
        bal_label.grid(row=2, column=0, sticky=W, padx=5)
        int_label.grid(row=3, column=0, sticky=W, padx=5)
        pymt_label.grid(row=4, column=0, sticky=W, padx=5)
        new_amt.grid(row=5, column=0, sticky=W, pady=10, padx=5)
        num.grid(row=6, column=0, sticky=W, pady=10, padx=5)

    #   Create and format entries in window
    def create_entries(self):
        self.master.title_entry = Entry(self.master)
        self.master.bal_entry = Entry(self.master)
        self.master.int_entry = Entry(self.master)
        self.master.pymt_entry = Entry(self.master)
        self.master.num_pymnts = Entry(self.master)
        self.master.new_pymnt = Entry(self.master)

        #   Format Entries
        self.master.title_entry.grid(row=1, column=1)
        self.master.bal_entry.grid(row=2, column=1)
        self.master.int_entry.grid(row=3, column=1)
        self.master.pymt_entry.grid(row=4, column=1)
        self.master.new_pymnt.grid(row=5, column=1)
        self.master.num_pymnts.grid(row=6, column=1)

    #   Create buttons, format, and assign commands
    def create_buttons(self):
        #   Connect to DB
        connect_button = Button(self.master, text="Connect to DB", command=self.connect_to_DB)
        connect_button.grid(row=1, column=2)

        #   Disconnect from DB
        disconnect_button = Button(self.master, text="Disconnect", command=self.close_DB)
        disconnect_button.grid(row=2, column=2)

        #   Click Start
        make_loan_button = Button(self.master, text="Start loan", command=self.make_loan)
        make_loan_button.grid(row=4, column=2, pady=5)

        #   Click Update Payment
        update_button = Button(self.master, text="Update Payment", command=self.update_payment)
        update_button.grid(row=5, column=2)

        #   Click Make Payments
        pay_button = Button(self.master, text="Make payments", command=self.pay_loan)
        pay_button.grid(row=6, column=2)

        #   Click Payoff
        payoff_button = Button(self.master, text="Payoff", command=self.payoff_loan)
        payoff_button.grid(row=7, column=0, sticky=W, pady=5)

        #   Click Display
        display_button = Button(self.master, text="Display history", command=self.display_info)
        display_button.grid(row=8, column=0, sticky=W, pady=5)

    #   Unpopulate entries in window
    def clear_entries(self):
        self.master.title_entry.delete(0, "end")
        self.master.bal_entry.delete(0, "end")
        self.master.int_entry.delete(0, "end")
        self.master.pymt_entry.delete(0, "end")
        self.master.new_pymnt.delete(0, "end")
        self.master.num_pymnts.delete(0, "end")


    ####################
    #   CONTROL
    ####################

    def connect_to_DB(self):
        try:
            self.my_connection = LoanDBConnector()
        except (NameError, mySQL.InterfaceError):
            print("Connection failed")
        else:
            print("Connection succeeded")
            self.start_db_scroller()

    def close_DB(self):
        if self.my_connection is not None:
            self.my_connection.close_connection()
            print("Connection closed")
        else:
            print("No connection to close")

    # Menu to load loan object from db into my_loan
    def start_db_scroller(self):
        #   Get active loan, populate fields in self.master(calc_window)
        def load_loan():
            try:
                index = l_list_box.curselection()
                selected = l_list_box.get(index)
            except TclError:
                print("Invalid selection")
            else:

                # Save current loan in memory before opening new
                self.loan_memory.append(self.my_loan)

                self.my_loan = StandardLoan(
                    float(selected[2]),
                    float(selected[3]),
                    float(selected[4]),
                    title=selected[1])

                self.my_loan._print_payment_info()

                #   Clear and populate entry fields
                self.clear_entries()
                self.master.title_entry.insert(0, f"{self.my_loan.title}")
                self.master.bal_entry.insert(0, self.my_loan.current_bal)
                self.master.int_entry.insert(0, self.my_loan.int_rate)
                self.master.pymt_entry.insert(0, self.my_loan.payment_amt)

        def clear_database():
            self.my_connection.wipe_db()

        #   Initialize Window
        #   Get 10 most recent loans, display db of loans in Listbox window
        l_list = self.my_connection.get_loans()
        db_scroller = Tk()
        l_list_box = Listbox(db_scroller, height=15, width=40, selectmode="SINGLE")
        db_scroller.geometry("500x300")
        db_scroller.title("Loans in database")

        for i in range(len(l_list)):
            l_list_box.insert(i, l_list[i])

        l_list_box.pack()

        # Buttons
        loan_button = Button(db_scroller, text="Load", command=load_loan)
        clear_db_button = Button(db_scroller, text="Clear", command=clear_database)
        loan_button.pack()
        clear_db_button.pack()

    #   Retrieve init data from fields, initialize new loan object
    def make_loan(self):
        try:
            title = str(self.master.title_entry.get())
            bal = float(self.master.bal_entry.get())
            i_rate = float(self.master.int_entry.get())
            m_payment = float(self.master.pymt_entry.get())
        except ValueError:
            messagebox.showinfo("Value Error",
                        "Make sure field entries are accurate")

        # Check for conneciton. If not, don't try to add to db
        else:
            self.my_loan = StandardLoan(bal, i_rate, m_payment, title=title)

            #   Add loan info to DB
            if self.my_connection:
                self.my_connection.add_loan_to_db(self.my_loan)
                print("Loan added to database")

    def update_payment(self):
        _p = self.master.new_pymnt.get()
        if self.master.new_pymnt.get() == "":
            return
        try:
            _p = float(self.master.new_pymnt.get())
            self.my_loan.payment_amt = _p
            self.master.pymt_entry.delete(0, "end")
            self.master.pymt_entry.insert(0, _p)
        except ValueError:
            messagebox.showinfo("Update Error",
                        "Make sure new payment amount is entered")

    def pay_loan(self):
        _n = self.master.num_pymnts.get()

        if self.my_loan.current_bal > 0:
            #   Get new payment amount, num of payments
            try:
                self.update_payment()
                self.my_loan.pay_months(int(_n))

            except ValueError:
                messagebox.showinfo("Payment Error",
                "Make sure number of payments and new payment amount is entered")
        else:
            messagebox.showinfo("Payment Error",
                        "Loan is already paid off")

    def payoff_loan(self):
        if self.my_loan.current_bal > 0:
            self.my_loan.payoff()

            #   Update payment history in DB
            if self.my_loan.current_bal > 0:
                messagebox.showinfo("Payment Error",
                            "Payments cannot cover interest, loan will never complete.")
            else:
                self.display_info()
        else:
            messagebox.showinfo("Payment Error",
                        "Loan is already paid off")

    @staticmethod
    def client_exit(self):
        exit()


    ####################
    #   PLOT
    ####################    

    def plot_Payment_History(self):
        #   Get data we need from Loan object using methods
        history = self.my_loan.Payment_History
        payments = self.my_loan.pay_no
        highest_bal = float(max(history["balance"]))
        #   PP yields a percentage /100
        #   Convert to current y scale
        pp_over_time = [(history["principal"][i+1] / (history["principal"][i+1]
                        + history["interest"][i+1]) * 100)
                        if history["principal"][i+1] != 0
                        else 0 for i in range(payments)]
        avg_pp = [sum(pp_over_time[0:i+1]) / (i+1) for i in range(payments)]

        #   Balance History data
        principal_history = [sum(history["principal"][0:i+1]) for i in range(payments+1)]
        interest_history = [sum(history["interest"][0:i+1]) for i in range(payments+1)]
        total_history = [principal_history[i] + interest_history[i] for i in range(payments+1)]

        ####################################
        #   Payment History Plot
        ####################################
        plt.figure(self.my_loan.title)

        #   Balance History Plots
        #   Define axes of graph based on Highest Balance and # Payments
        balance_graph = plt.subplot(3, 1, 1)
        plt.title("Balance History")
        plt.ylabel("$")
        plt.xlabel("Payment #")
        if highest_bal >= self.my_loan.get_total_paid():
            plt.axis([0, payments, 0, highest_bal])
        else:
            plt.axis([0, payments, 0, float(self.my_loan.get_total_paid())])
        balance_graph.plot("balance", data=history)
        balance_graph.plot(principal_history, label="total principal paid")
        balance_graph.plot(interest_history, label="total interest paid")
        balance_graph.plot(total_history, label="total paid")
        plt.legend()

        # Monthly Plots
        monthly_graph = plt.subplot(3, 1, 2)
        plt.title("Payment History")
        plt.ylabel("$")
        plt.xlabel("Payment #")

        monthly_graph.bar(history["pay_no"], history["principal"], label="Towards principal")
        monthly_graph.bar(history["pay_no"], history["interest"], label="Towards interest")
        plt.legend()

        # Principal Efficiency Plots
        # Ddd zeroes to front of percenetages to scale to graph
        pp_over_time.insert(0, 0)
        avg_pp.insert(0, 0)
        interest_graph = plt.subplot(3, 1, 3)
        plt.title("Principal Efficiency")
        plt.ylabel("%")
        plt.xlabel("Payment #")
        # If percentages are 0, display so
        if sum(pp_over_time) == 0:
            plt.axis([0, payments, -1, 1])
        else:
            plt.axis([0, payments, 0, 100])
        interest_graph.plot(pp_over_time, label="% of payment towards principal")
        interest_graph.plot(avg_pp, label="average % towards principal")
        plt.legend()

        # Show
        plt.tight_layout()
        plt.show()

    def display_info(self):
        if self.my_loan.pay_no > 0:
            all_info = Tk()
            all_info.geometry("300x200")
            all_info.title("Loan Information")
            my_info = self.my_loan.get_payment_info()

            for i in range(len(my_info)):
                Label(all_info, text=f"{my_info[i]}").grid(row=i+1, column=1, sticky=W)

            self.plot_Payment_History()
        else:
            messagebox.showinfo("Display Error",
                                "Nothing to display")

    

