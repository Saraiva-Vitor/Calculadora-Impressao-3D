import tkinter as tk
from tkinter import messagebox
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def validar_float(P):
    try:
        if not P or P == ".":
            return True
        float(P)
        return True
    except ValueError:
        messagebox.showinfo("Aviso", "Por favor, insira apenas números.")
        return False

def calcular_orcamento():
    try:
        tempo_impressao = float(tempo_impressao_entry.get())
        valor_kgfilamento = float(valor_vfilamentokg_entry.get())
        total_filamento = float(total_filamento_entry.get())

        total_filamento_kg = total_filamento/1000
        pot_equip = 300/1000

        custo_energia = pot_equip * tempo_impressao * 1.1
        custo_filamento = valor_kgfilamento * total_filamento_kg
        custo_total = custo_energia + custo_filamento
        custo_total_maoobra = custo_total + 1.5*custo_total

        resultados = f"Custo de Energia: R$ {custo_energia:.2f}\nCusto de Material: R$ {custo_filamento:.2f}\nCusto Total: R$ {custo_total:.2f}\nCusto Total Com Mão de Obra: R$ {custo_total_maoobra:.2f}"
        resultado_label.config(text=resultados)
        
        export_to_pdf(resultados)

    except ValueError:
        resultado_label.config(text="Por favor, insira valores numéricos.")

def adicionar_texto_pdf(pdf_existente, texto):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Dividir o texto em linhas com quebra de linha
    linhas_de_texto = texto.split('\n')
    
    y = 600
    for line in linhas_de_texto:
        c.drawString(100, y, line)
        y -= 20  # Espaçamento entre as linhas

    c.save()

    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    text_page = new_pdf.pages[0]

    with open(pdf_existente, 'rb') as pdf_antigo:
        reader = PyPDF2.PdfReader(pdf_antigo)
        writer = PyPDF2.PdfWriter()

        for i in range(len(reader.pages)):
            page = reader.pages[i]
            page.merge_page(text_page)
            writer.add_page(page)

        with open('Orçamento.pdf', 'wb') as pdf_novo:
            writer.write(pdf_novo)

def export_to_pdf(resultados):
    adicionar_texto_pdf('Modelo Orçamento.pdf', resultados)
    messagebox.showinfo("Exportar", "Resultados exportados para 'Orçamento.pdf'")

root = tk.Tk()
root.title("Calculadora de Orçamento de Impressão 3D")

vcmd = root.register(validar_float)

# Frames para organizar a interface
input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=10)

resultado_frame = tk.Frame(root)
resultado_frame.pack(padx=20, pady=10)

# Campos de entrada
tk.Label(input_frame, text="Tempo de Impressão (horas):").grid(row=0, column=0)
tempo_impressao_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd, '%P'))
tempo_impressao_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Valor do Filamento (R$/Kg):").grid(row=1, column=0)
valor_vfilamentokg_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd, '%P'))
valor_vfilamentokg_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Total de Filamento utilizado (gramas):").grid(row=2, column=0)
total_filamento_entry = tk.Entry(input_frame, validate="key", validatecommand=(vcmd, '%P'))
total_filamento_entry.grid(row=2, column=1)

# Resultado
resultado_label = tk.Label(resultado_frame, text="")
resultado_label.pack()

exportar_button = tk.Button(resultado_frame, text="Exportar Resultados", command=calcular_orcamento)
exportar_button.pack()

root.mainloop()
