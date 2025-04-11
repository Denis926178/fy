import os
import shutil

from security import SecurityManager

class FileManager:
    def __init__(self, base_dir):
        self.base_dir = os.path.abspath(base_dir)
        self.current_dir = self.base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
    
    def __get_full_path(self, path):
        return os.path.abspath(os.path.join(self.current_dir, path))
    
    def create_dir(self, name):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{name}' created.")
    
    def remove_dir(self, name):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        shutil.rmtree(path)
        print(f"Directory '{name}' removed.")
    
    def change_dir(self, name):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        if os.path.isdir(path):
            self.current_dir = path
            print(f"Changed directory to '{self.current_dir}'.")
        else:
            print("Invalid directory.")
    
    def list_dir(self):
        print("Contents of", self.current_dir)
        for item in os.listdir(self.current_dir):
            print(item)
    
    def print_working_directory(self):
        print(f"Current directory: {self.current_dir}")

    def create_file(self, name, content=""):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        with open(path, 'w') as f:
            f.write(content)
        print(f"File '{name}' created.")
    
    def read_file(self, name):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        with open(path, 'r') as f:
            print(f.read())
    
    def write_file(self, name, content):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        with open(path, 'a') as f:
            f.write(content + '\n')
        print(f"Written to file '{name}'.")
    
    def delete_file(self, name):
        path = SecurityManager.get_absolute_path(self.__get_full_path(name))
        os.remove(path)
        print(f"File '{name}' deleted.")
    
    def copy_file(self, src, dst):
        src_path = SecurityManager.get_absolute_path(self.__get_full_path(src))
        dst_path = SecurityManager.get_absolute_path(self.__get_full_path(dst))
        shutil.copy2(src_path, dst_path)
        print(f"File '{src}' copied to '{dst}'.")
    
    def move_file(self, src, dst):
        src_path = SecurityManager.get_absolute_path(self.__get_full_path(src))
        dst_path = SecurityManager.get_absolute_path(self.__get_full_path(dst))
        shutil.move(src_path, dst_path)
        print(f"File '{src}' moved to '{dst}'.")
    
    def rename_file(self, old_name, new_name):
        old_path = SecurityManager.get_absolute_path(self.__get_full_path(old_name))
        new_path = SecurityManager.get_absolute_path(self.__get_full_path(new_name))
        os.rename(old_path, new_path)
        print(f"File '{old_name}' renamed to '{new_name}'.")
    
    def run(self):
        while True:
            command = input("fm> ").strip().split()
            if not command:
                continue
            cmd, *args = command
            try:
                if cmd == "mkdir":
                    self.create_dir(*args)
                elif cmd == "rmdir":
                    self.remove_dir(*args)
                elif cmd == "cd":
                    self.change_dir(*args)
                elif cmd == "ls":
                    self.list_dir()
                elif cmd == "pwd":
                    self.print_working_directory()
                elif cmd == "touch":
                    self.create_file(*args)
                elif cmd == "cat":
                    self.read_file(*args)
                elif cmd == "write":
                    self.write_file(*args)
                elif cmd == "rm":
                    self.delete_file(*args)
                elif cmd == "cp":
                    self.copy_file(*args)
                elif cmd == "mv":
                    self.move_file(*args)
                elif cmd == "rename":
                    self.rename_file(*args)
                elif cmd == "exit":
                    print("Exiting file manager.")
                    break
                else:
                    print("Unknown command.")
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    fm = FileManager(SecurityManager().start_path())
    fm.run()
