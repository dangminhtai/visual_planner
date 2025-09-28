import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import calendar
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

class VisualPlannerApp:
    def __init__(self, root):
            self.root = root
            self.root.title("Visual Planner")
            from datetime import datetime
            now = datetime.now()
            current_month = now.month
            current_year = now.year

            # Chọn tháng bắt đầu
            ttk.Label(root, text="Start Month:").grid(row=0, column=0, padx=5, pady=5)
            self.start_month = ttk.Combobox(root, values=list(range(1, 13)), width=5)
            self.start_month.set(current_month)   # gán tháng hiện tại
            self.start_month.grid(row=0, column=1, padx=5, pady=5)

            # Chọn năm
            ttk.Label(root, text="Year:").grid(row=0, column=2, padx=5, pady=5)
            self.year_entry = ttk.Entry(root, width=6)
            self.year_entry.insert(0, str(current_year))  # gán năm hiện tại
            self.year_entry.grid(row=0, column=3, padx=5, pady=5)

            # Chọn số tháng liên tiếp
            ttk.Label(root, text="Months Count:").grid(row=0, column=4, padx=5, pady=5)
            self.month_count = ttk.Combobox(root, values=list(range(1, 13)), width=5)
            self.month_count.current(0)
            self.month_count.grid(row=0, column=5, padx=5, pady=5)

            # Nút preview
            ttk.Button(root, text="Preview", command=self.show_preview).grid(row=0, column=6, padx=5, pady=5)

            # Nút lưu PDF
            ttk.Button(root, text="Save as PDF", command=self.save_pdf).grid(row=0, column=7, padx=5, pady=5)

            # Frame để hiện lịch preview
            self.preview_frame = tk.Frame(root)
            self.preview_frame.grid(row=1, column=0, columnspan=8, padx=10, pady=10)

    def show_preview(self):
        # Clear preview cũ
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        start_month = int(self.start_month.get())
        year = int(self.year_entry.get())
        months_count = int(self.month_count.get())

        for i in range(months_count):
            month = (start_month + i - 1) % 12 + 1
            year_offset = (start_month + i - 1) // 12
            current_year = year + year_offset

            cal = calendar.Calendar(firstweekday=0)
            month_days = cal.monthdayscalendar(current_year, month)

            frame = tk.LabelFrame(self.preview_frame, text=f"{calendar.month_name[month]} {current_year}")
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)

            # Header
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for j, d in enumerate(days):
                tk.Label(frame, text=d, width=5, borderwidth=1, relief="solid").grid(row=0, column=j)

            # Dates
            for r, week in enumerate(month_days, start=1):
                for c, day in enumerate(week):
                    if day == 0:
                        txt = ""
                    else:
                        txt = str(day)
                    tk.Label(frame, text=txt, width=5, height=2, borderwidth=1, relief="solid").grid(row=r, column=c)



    def save_pdf(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file_path:
            return

        start_month = int(self.start_month.get())
        year = int(self.year_entry.get())
        months_count = int(self.month_count.get())

        page_w, page_h = landscape(letter)
        margin = 40

        c = canvas.Canvas(file_path, pagesize=(page_w, page_h))

        for i in range(months_count):
            month = (start_month + i - 1) % 12 + 1
            year_offset = (start_month + i - 1) // 12
            current_year = year + year_offset

            cal = calendar.Calendar(firstweekday=0)
            month_days = cal.monthdayscalendar(current_year, month)

            # --- Title ---
            title_font_size = 20
            c.setFont("Helvetica-Bold", title_font_size)
            title_y = page_h - margin
            c.drawCentredString(page_w / 2, title_y, f"{calendar.month_name[month]} {current_year}")

            # --- Table layout ---
            gap = 40  # khoảng cách giữa baseline của title và đỉnh bảng (bạn có thể chỉnh)
            table_top_y = title_y - title_font_size - gap  # đây là "đỉnh" của bảng (y lớn hơn)
            table_w = page_w - 2 * margin
            table_h = table_top_y - margin  # khoảng cao từ đỉnh bảng xuống lề dưới
            cell_w = table_w / 7
            cell_h = table_h / (len(month_days) + 1)  # +1 cho header row

            x_start = margin
            y_top = table_top_y  # tên rõ ràng: y_top = đỉnh của bảng

            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

            # --- Header row ---
            c.setFont("Helvetica-Bold", 10)
            header_bottom_y = y_top - cell_h  # bottom của ô header
            for j, d in enumerate(days):
                x = x_start + j * cell_w
                y = header_bottom_y
                c.rect(x, y, cell_w, cell_h)
                c.drawCentredString(x + cell_w / 2, y + cell_h / 2 - 3, d)

            # --- Days ---
            # Với mỗi tuần r (0-based), bottom y = y_top - (r + 2) * cell_h
            # (vì header đã chiếm 1 hàng)
            c.setFont("Helvetica", 8)
            for r, week in enumerate(month_days):
                for cidx, day in enumerate(week):
                    x = x_start + cidx * cell_w
                    y = y_top - (r + 2) * cell_h
                    c.rect(x, y, cell_w, cell_h)
                    if day != 0:
                        c.drawString(x + 3, y + cell_h - 10, str(day))

            c.showPage()

        c.save()
        messagebox.showinfo("Success", "Planner saved as PDF!")



if __name__ == "__main__":
    root = tk.Tk()
    app = VisualPlannerApp(root)
    root.mainloop()
