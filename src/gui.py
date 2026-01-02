"""
Interface gráfica simples com tkinter,
listar autores em messagebox,
login para relatórios com janela separada,
chamo funções de crud, management e reports
"""

import tkinter as tk
from tkinter import messagebox
import crud
import management
import reports

def listar_autores():
    autores = crud.load_autores()
    # Formato bonito para mostrar
    texto = "\n".join([f"{a['artist_name']} - {a['artist_nacionality']}" for a in autores.values()])
    messagebox.showinfo("Autores", texto)

def realizar_login_gui(username, password):
    # Adaptação de realizar_login para GUI, sem input
    for admin in management.lista_admins:
        if admin["username"] == username and admin["password"] == password:
            return True
    return False

def login_relatorios():
    janela_login = tk.Toplevel()
    janela_login.title("Login")

    tk.Label(janela_login, text="Utilizador").pack()
    user = tk.Entry(janela_login)
    user.pack()

    tk.Label(janela_login, text="Senha").pack()
    pwd = tk.Entry(janela_login, show="*")
    pwd.pack()

    def validar():
        if realizar_login_gui(user.get(), pwd.get()):
            janela_login.destroy()
            relatorio = reports.gerar_relatorio()
            messagebox.showinfo("Relatório", relatorio)
        else:
            messagebox.showerror("Erro", "Login inválido")

    tk.Button(janela_login, text="Entrar", command=validar).pack()

def main_gui():
    root = tk.Tk()
    root.title("Editora Tocadiscos")

    tk.Button(root, text="Autores", width=30, command=listar_autores).pack(pady=5)
    tk.Button(root, text="Relatórios", width=30, command=login_relatorios).pack(pady=5)
    tk.Button(root, text="Sair", width=30, command=root.quit).pack(pady=5)

    root.mainloop()