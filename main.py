
import customtkinter as ctk
import json
from tkinter import filedialog

class RPGTaskManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RPG Task Manager")
        self.geometry("900x600")
        self.configure(fg_color=("#2E3440", "#3B4252"))
        
        self.tasks = []
        self.skills_list = ["Aprendizado", "Erudição", "Leitura", "Resistência", "Criatividade", "Liderança", "Disciplina", "Comunicação", "Lógica", "Resolução de Problemas"]
        self.player_data = {
            "name": "Jogador",
            "level": 1,
            "xp": 0,
            "xp_next_level": 100,
            "coins": 0,
            "attributes": {
                "Força": 1,
                "Inteligência": 1,
                "Disciplina": 1,
                "Felicidade": 1,
                "Saúde": 1
            },
            "skills": {skill: 0 for skill in self.skills_list}
        }
        
        self.create_ui()
        
    def create_ui(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.task_label = ctk.CTkLabel(frame, text="Nova Tarefa:")
        self.task_label.pack()
        
        self.task_entry = ctk.CTkEntry(frame)
        self.task_entry.pack()
        
        self.importance_label = ctk.CTkLabel(frame, text="Importância:")
        self.importance_label.pack()
        self.importance_options = ["Pouco Importante", "Importante", "Muito Importante"]
        self.importance_var = ctk.StringVar(value=self.importance_options[0])
        self.importance_dropdown = ctk.CTkOptionMenu(frame, variable=self.importance_var, values=self.importance_options)
        self.importance_dropdown.pack()
        
        self.difficulty_label = ctk.CTkLabel(frame, text="Dificuldade:")
        self.difficulty_label.pack()
        self.difficulty_options = ["Muito Fácil", "Fácil", "Médio", "Difícil", "Muito Difícil", "Impossível"]
        self.difficulty_var = ctk.StringVar(value=self.difficulty_options[0])
        self.difficulty_dropdown = ctk.CTkOptionMenu(frame, variable=self.difficulty_var, values=self.difficulty_options)
        self.difficulty_dropdown.pack()
        
        self.skills_label = ctk.CTkLabel(frame, text="Habilidades Relacionadas:")
        self.skills_label.pack()
        self.skills_selected = []
        self.skills_checkbuttons = {}
        
        for skill in self.skills_list:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(frame, text=skill, variable=var)
            cb.pack()
            self.skills_checkbuttons[skill] = var
        
        self.add_task_button = ctk.CTkButton(frame, text="Adicionar Tarefa", command=self.add_task)
        self.add_task_button.pack()
        
        self.task_listbox = ctk.CTkTextbox(frame, width=500, height=200)
        self.task_listbox.pack()
        
        self.complete_task_button = ctk.CTkButton(frame, text="Marcar como Concluída", command=self.complete_task)
        self.complete_task_button.pack()
        
        self.delete_task_button = ctk.CTkButton(frame, text="Excluir Tarefa", command=self.delete_task)
        self.delete_task_button.pack()
        
        self.export_button = ctk.CTkButton(frame, text="Exportar Dados", command=self.export_data)
        self.export_button.pack()
        
        self.import_button = ctk.CTkButton(frame, text="Importar Dados", command=self.import_data)
        self.import_button.pack()
        
        self.status_label = ctk.CTkLabel(frame, text=self.get_status_text())
        self.status_label.pack()
        
        self.skills_frame = ctk.CTkFrame(frame)
        self.skills_frame.pack(pady=10)
        self.create_skill_cards()

    def create_skill_cards(self):
        for skill in self.skills_list:
            btn = ctk.CTkButton(self.skills_frame, text=skill, command=lambda s=skill: self.open_skill_window(s))
            btn.pack(side="left", padx=5, pady=5)

    def open_skill_window(self, skill):
        skill_window = ctk.CTkToplevel(self)
        skill_window.title(skill)
        skill_window.geometry("300x200")

        impact = {"Aprendizado": {"Desenvolvimento Pessoal": 100, "Inteligência": 90},
                  "Resistência": {"Saúde": 80, "Disciplina": 70}}
        xp = self.player_data["skills"].get(skill, 0)
        xp_next = 100  # Valor arbitrário para próximo nível
        
        info_label = ctk.CTkLabel(skill_window, text=f"XP: {xp}/{xp_next}")
        info_label.pack()
        
        impact_label = ctk.CTkLabel(skill_window, text=f"Impacto:")
        impact_label.pack()
        
        for key, value in impact.get(skill, {}).items():
            impact_info = ctk.CTkLabel(skill_window, text=f"{key}: {value}%")
            impact_info.pack()
        
    def get_status_text(self):
        return (f"Nome: {self.player_data['name']}\n"
                f"Nível: {self.player_data['level']}\n"
                f"XP: {self.player_data['xp']}/{self.player_data['xp_next_level']}\n"
                f"Moedas: {self.player_data['coins']}\n")
        
    def add_task(self):
        task_name = self.task_entry.get()
        if task_name:
            selected_skills = [skill for skill, var in self.skills_checkbuttons.items() if var.get()]
            task = {
                "name": task_name,
                "importance": self.importance_var.get(),
                "difficulty": self.difficulty_var.get(),
                "skills": selected_skills,
                "completed": False
            }
            self.tasks.append(task)
            self.task_entry.delete(0, "end")
            self.update_task_listbox()
        
    def update_task_listbox(self):
        self.task_listbox.delete("1.0", "end")
        for task in self.tasks:
            status = "✔" if task["completed"] else "✖"
            self.task_listbox.insert("end", f"[{status}] {task['name']} - {task['importance']} - {task['difficulty']}\n")
        
    def complete_task(self):
        for task in self.tasks:
            if not task["completed"]:
                task["completed"] = True
                self.player_data["xp"] += 10
                self.player_data["coins"] += 5
                for skill in task["skills"]:
                    self.player_data["skills"][skill] += 5
                self.check_level_up()
        self.update_task_listbox()
        self.status_label.configure(text=self.get_status_text())
        
    def delete_task(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_task_listbox()
        
    def check_level_up(self):
        if self.player_data["xp"] >= self.player_data["xp_next_level"]:
            self.player_data["xp"] -= self.player_data["xp_next_level"]
            self.player_data["level"] += 1
            self.player_data["xp_next_level"] *= 1.5
            self.status_label.configure(text=self.get_status_text())
        
    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump({"tasks": self.tasks, "player_data": self.player_data}, file, indent=4)
        
    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.tasks = data["tasks"]
                self.player_data = data["player_data"]
            self.update_task_listbox()
            self.status_label.configure(text=self.get_status_text())
        
if __name__ == "__main__":
    app = RPGTaskManager()
    app.mainloop()
