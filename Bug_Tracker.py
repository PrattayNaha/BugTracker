import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os
import shutil
from PIL import Image, ImageTk
from datetime import datetime


class BugManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bug Tracker Pro - Enterprise Edition")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f2f5")

        self.DATA_FILE = "Bug_Report_PrattayNaha.xlsx"
        self.IMAGE_FOLDER = "bug_assets"

        if not os.path.exists(self.IMAGE_FOLDER):
            os.makedirs(self.IMAGE_FOLDER)

        self.create_home_screen()

    def create_home_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("600x500")

        tk.Label(self.root, text="Bug Management System", font=("Segoe UI", 20, "bold"), bg="#f0f2f5",
                 fg="#38669b").pack(pady=30)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 30, "pady": 8, "cursor": "hand2"}

        tk.Button(self.root, text="➕ Enter Bug Report Data", command=lambda: self.open_bug_form(),
                  bg="#38669b", fg="white", **btn_style).pack(pady=5)

        tk.Button(self.root, text="📥 Import External XLSX", command=self.import_external_xlsx,
                  bg="#28a745", fg="white", **btn_style).pack(pady=5)

        tk.Button(self.root, text="📊 See Structural Report", command=self.open_report_view,
                  bg="#ffffff", fg="#38669b", **btn_style).pack(pady=5)

    # --- IMPORT FEATURE ---
    def import_external_xlsx(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            ext_df = pd.read_excel(file_path)

            # Mapping your Test_Cases.xlsx columns to App columns
            # Adjust these strings if your Excel headers are different
            column_mapping = {
                'ID': 'bug_id',
                'Test Case': 'title',
                'Steps': 'steps',
                'Expected Result': 'expected',
                'Actual Result': 'actual',
                'Status': 'Severity'
            }

            # Rename columns to match our internal database
            imported_df = ext_df.rename(columns=column_mapping)

            # Add missing columns with default values
            if 'issue_type' not in imported_df.columns:
                imported_df['issue_type'] = "Imported"
            if 'Image_Path' not in imported_df.columns:
                imported_df['Image_Path'] = "No Image"
            if 'Timestamp' not in imported_df.columns:
                imported_df['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Keep only the columns we use in the app
            valid_cols = ['issue_type', 'bug_id', 'title', 'steps', 'expected', 'actual', 'Severity', 'Image_Path',
                          'Timestamp']
            imported_df = imported_df[[c for c in valid_cols if c in imported_df.columns]]

            # Merge with existing data
            if os.path.exists(self.DATA_FILE):
                main_df = pd.read_excel(self.DATA_FILE)
                final_df = pd.concat([main_df, imported_df], ignore_index=True).drop_duplicates(subset=['bug_id'],
                                                                                                keep='last')
            else:
                final_df = imported_df

            final_df.to_excel(self.DATA_FILE, index=False)
            messagebox.showinfo("Import Success", f"Successfully imported {len(imported_df)} records.")

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to process file:\n{e}")

    # --- REUSABLE FORM ---
    def open_bug_form(self, edit_data=None):
        self.form_win = tk.Toplevel(self.root)
        self.form_win.title("Edit Bug Report" if edit_data else "Report New Bug")
        self.form_win.geometry("600x750")

        # In your previous code, edit_data[7] was image path.
        # With "Issue Type" added, your columns increased. Let's make it dynamic.
        self.image_path = edit_data[7] if (edit_data and len(edit_data) > 7) else ""

        fields = [("Issue Type", "issue_type"), ("Bug ID:", "bug_id"), ("Bug Title:", "title"),
                  ("Steps:", "steps"), ("Expected:", "expected"), ("Actual:", "actual")]
        self.inputs = {}

        for i, (label_text, key) in enumerate(fields):
            frame = tk.Frame(self.form_win)
            frame.pack(fill="x", padx=30, pady=5)
            tk.Label(frame, text=label_text, font=("Segoe UI", 10, "bold")).pack(anchor="w")

            if key == "steps":
                entry = tk.Text(frame, height=4, font=("Segoe UI", 10))
                if edit_data: entry.insert("1.0", str(edit_data[i]))
            else:
                entry = tk.Entry(frame, font=("Segoe UI", 10))
                if edit_data: entry.insert(0, str(edit_data[i]))
                if key == "bug_id" and edit_data: entry.config(state="disabled")

            entry.pack(fill="x")
            self.inputs[key] = entry

        frame = tk.Frame(self.form_win);
        frame.pack(fill="x", padx=30, pady=5)
        tk.Label(frame, text="Severity:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.severity_var = tk.StringVar(value=edit_data[6] if edit_data else "Low")
        ttk.Combobox(frame, textvariable=self.severity_var, values=["Low", "Medium", "High"], state="readonly").pack(
            fill="x")

        tk.Button(self.form_win, text="📸 Upload Screenshot", command=self.upload_image).pack(pady=10)
        self.img_label = tk.Label(self.form_win,
                                  text=os.path.basename(self.image_path) if self.image_path else "No image", fg="gray")
        self.img_label.pack()

        btn_text = "UPDATE REPORT" if edit_data else "SAVE REPORT"
        tk.Button(self.form_win, text=btn_text, command=lambda: self.save_data(is_edit=bool(edit_data)),
                  bg="#28a745", fg="white", font=("Segoe UI", 12, "bold"), width=20).pack(pady=20)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if path:
            self.image_path = path
            self.img_label.config(text=os.path.basename(path), fg="green")

    def save_data(self, is_edit=False):
        data = {k: (v.get("1.0", "end-1c") if isinstance(v, tk.Text) else v.get()) for k, v in self.inputs.items()}
        data["Severity"] = self.severity_var.get()
        data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        if self.image_path and os.path.exists(self.image_path):
            if "bug_assets" not in self.image_path:
                ext = os.path.splitext(self.image_path)[1]
                dest = os.path.join(self.IMAGE_FOLDER, f"{data['bug_id']}{ext}")
                shutil.copy(self.image_path, dest)
                data["Image_Path"] = dest
            else:
                data["Image_Path"] = self.image_path
        else:
            data["Image_Path"] = "No Image"

        df = pd.read_excel(self.DATA_FILE) if os.path.exists(self.DATA_FILE) else pd.DataFrame()

        if is_edit:
            df.loc[df['bug_id'].astype(str) == str(data['bug_id']), data.keys()] = data.values()
        else:
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

        df.to_excel(self.DATA_FILE, index=False)
        messagebox.showinfo("Success", "Data synchronized!")
        self.form_win.destroy()
        if hasattr(self, 'report_win') and self.report_win.winfo_exists():
            self.refresh_report()

    # --- REPORT VIEW ---
    def open_report_view(self):
        self.report_win = tk.Toplevel(self.root)
        self.report_win.title("Structural Bug Report")
        self.report_win.geometry("1200x650")

        btn_frame = tk.Frame(self.report_win, pady=10)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="✏️ Edit Selected", command=self.edit_selected, bg="#ffc107", width=15).pack(
            side="left", padx=10)
        tk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_selected, bg="#dc3545", fg="white",
                  width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="📥 Download XLSX", command=self.download_report, bg="#17a2b8", fg="white",
                  width=15).pack(side="right", padx=10)

        self.tree = ttk.Treeview(self.report_win, show="headings")
        self.tree.pack(expand=True, fill="both", padx=10)
        self.refresh_report()

    def refresh_report(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        if os.path.exists(self.DATA_FILE):
            df = pd.read_excel(self.DATA_FILE)
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

    def edit_selected(self):
        try:
            item_id = self.tree.selection()[0]
            selected_values = self.tree.item(item_id)["values"]
            self.open_bug_form(edit_data=selected_values)
        except IndexError:
            messagebox.showwarning("Selection", "Please select a row to edit.")

    def delete_selected(self):
        try:
            item_id = self.tree.selection()[0]
            # FIX: We find the index of the 'bug_id' column dynamically
            columns = self.tree["columns"]
            bug_id_index = columns.index('bug_id')
            bug_id_value = self.tree.item(item_id)["values"][bug_id_index]

            if messagebox.askyesno("Confirm", f"Delete Bug ID: {bug_id_value}?"):
                df = pd.read_excel(self.DATA_FILE)
                # Ensure we compare strings to strings
                df = df[df['bug_id'].astype(str) != str(bug_id_value)]
                df.to_excel(self.DATA_FILE, index=False)
                self.refresh_report()
                messagebox.showinfo("Deleted", "Record removed.")
        except IndexError:
            messagebox.showwarning("Selection", "Please select a row to delete.")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def download_report(self):
        if not os.path.exists(self.DATA_FILE): return
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            df = pd.read_excel(self.DATA_FILE)
            if "Image_Path" in df.columns: df = df.drop(columns=["Image_Path"])
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Export Successful", "Report saved.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BugManagerApp(root)
    root.mainloop()