import tkinter as tk
from tkinter import filedialog, messagebox
from converters import available_converters
from PIL import Image, ImageTk


def center_window(win, width=600, height=400):
    win.update_idletasks()  # На всякий случай, чтобы tkinter знал реальные размеры

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")


def show_welcome():
    welcome_win = tk.Tk()
    welcome_win.title("Добро пожаловать!")
    welcome_win.configure(bg="#f0f0f0")
    center_window(welcome_win, width=600, height=300)

    # Основной контейнер
    frame = tk.Frame(welcome_win, bg="#f0f0f0")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Левая часть — картинка
    img = Image.open(r"E:\Dev\cmbelazy\resources\welcome.png").resize((150, 150))  # Уменьшаем прямо здесь
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(frame, image=photo, bg="#f0f0f0")
    img_label.image = photo  # важно сохранить ссылку
    img_label.pack(side="left", padx=10, pady=10)

    # Правая часть — текст и кнопка
    text_frame = tk.Frame(frame, bg="#f0f0f0")
    text_frame.pack(side="left", fill="both", expand=True, padx=10)

    tk.Label(
        text_frame,
        text="Добро пожаловать в CMBeLazy!",
        bg="#f0f0f0",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
        justify="left",
        wraplength=350
    ).pack(anchor="w", pady=(10, 5))

    tk.Label(
        text_frame,
        text="Здесь вы можете конвертировать DOCX в HTML в разных форматах.\n\nВыберите способ конвертации, укажите файл и получите чистый HTML!",
        bg="#f0f0f0",
        font=("Segoe UI", 11),
        anchor="w",
        justify="left",
        wraplength=350
    ).pack(anchor="w", pady=(0, 20))

    tk.Button(
        text_frame,
        text="Приступить",
        font=("Segoe UI", 11, "bold"),
        bg="#2d574f",
        fg="white",
        activebackground="#7ac3bc",
        padx=15,
        pady=5,
        command=welcome_win.destroy
    ).pack(anchor="center")

    welcome_win.mainloop()


def start_gui():
    root = tk.Tk()
    root.title("CMBeLazy")
    root.iconbitmap(r"E:\Dev\cmbelazy\resources\logo.ico")
    center_window(root, width=500, height=250)

    # Основной фрейм
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(main_frame,
             text="Выберите тип конвертации:",
             bg="#f0f0f0",
             font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))

    converter_var = tk.StringVar(root)
    converter_var.set(next(iter(available_converters)))

    option_menu = tk.OptionMenu(main_frame, converter_var, *available_converters.keys())
    option_menu.config(
        font=("Segoe UI", 11),
        bg="#ffffff",
        fg="#333333",
        activebackground="#7ac3bc",
        activeforeground="#ffffff",
        highlightthickness=1,
        bd=1,
        relief="groove",
        width=25
        )
    option_menu["menu"].config(
        font=("Segoe UI", 11),
        bg="#ffffff",
        fg="#333333",
        activebackground="#7ac3bc",
        activeforeground="#ffffff"
        )
    option_menu.pack(pady=(0, 20))

    def run_conversion():
        selected = converter_var.get()
        converter = available_converters.get(selected)

        if converter is None:
            messagebox.showerror("Ошибка", "Выберите способ конвертации.")
            return

        def choose_file(prompt, save=False, **kwargs):
            dialog = filedialog.asksaveasfilename if save else filedialog.askopenfilename
            return dialog(title=prompt, **kwargs)

        input_path = choose_file(
            "Выберите DOCX файл",
            filetypes=[("Word документы", "*.docx")]
        )
        if not input_path:
            return

        output_path = choose_file(
            "Сохранить HTML как...",
            save=True,
            defaultextension=".html",
            filetypes=[("HTML файлы", "*.html")]
        )
        if not output_path:
            return

        try:
            converter.convert(input_path, output_path)
            messagebox.showinfo("Готово", "Файл успешно сконвертирован!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(main_frame,
              text="Конвертировать",
              font=("Segoe UI", 11, "bold"),
              bg="#7ac3bc",
              fg="white",
              activebackground="#2d574f",
              padx=10,
              pady=5,
              command=run_conversion).pack()

    root.mainloop()


if __name__ == "__main__":
    import traceback
    try:
        show_welcome()
        start_gui()
    except Exception:
        print("Ошибка при запуске GUI:")
        traceback.print_exc()
        input("Нажмите Enter, чтобы выйти...")
