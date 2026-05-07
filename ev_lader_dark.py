import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import threading
import time
from plyer import notification

class EVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EV Laad Monitor")
        self.root.geometry("350x350")
        
        # UI Elementen
        tk.Label(root, text="Resterende laadtijd", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(root, text="Uren:").pack()
        self.entry_uren = tk.Entry(root, justify='center')
        self.entry_uren.pack()

        tk.Label(root, text="Minuten:").pack()
        self.entry_minuten = tk.Entry(root, justify='center')
        self.entry_minuten.pack()

        self.btn_start = tk.Button(root, text="Start Laden", command=self.start_timer, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
        self.btn_start.pack(pady=15)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(pady=10)

        self.lbl_eindtijd = tk.Label(root, text="", font=("Arial", 12))
        self.lbl_eindtijd.pack()

        self.lbl_countdown = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="#0078d7")
        self.lbl_countdown.pack(pady=5)

    def start_timer(self):
        try:
            uren = int(self.entry_uren.get() or 0)
            minuten = int(self.entry_minuten.get() or 0)
            totaal_seconden = (uren * 3600) + (minuten * 60)

            if totaal_seconden <= 0:
                return

            nu = datetime.now()
            eindtijd = nu + timedelta(seconds=totaal_seconden)
            
            self.lbl_eindtijd.config(text=f"Verwacht 100% geladen om: {eindtijd.strftime('%H:%M:%S')}")
            self.btn_start.config(state="disabled") # Voorkom dubbel klikken

            # Start updates in een aparte thread
            threading.Thread(target=self.update_loop, args=(totaal_seconden,), daemon=True).start()

        except ValueError:
            messagebox.showerror("Fout", "Voer a.u.b. alleen cijfers in.")

    def update_loop(self, totaal_seconden):
        verstreken = 0
        while verstreken <= totaal_seconden:
            # Update voortgangsbalk (percentage)
            percentage = (verstreken / totaal_seconden) * 100
            self.progress['value'] = percentage
            
            # Update countdown tekst
            resterend = totaal_seconden - verstreken
            mins, secs = divmod(resterend, 60)
            hrs, mins = divmod(mins, 60)
            self.lbl_countdown.config(text=f"Nog: {hrs:02d}:{mins:02d}:{secs:02d}")
            
            time.sleep(1)
            verstreken += 1

        # Klaar!
        self.lbl_countdown.config(text="Batterij Vol! ⚡", fg="#28a745")
        notification.notify(
            title="EV Opgeladen! ⚡",
            message="Je auto is nu 100% vol.",
            timeout=10
        )
        self.btn_start.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = EVApp(root)
    root.mainloop()
