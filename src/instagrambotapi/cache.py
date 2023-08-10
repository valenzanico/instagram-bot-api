import json
import os
import time
from contextlib import contextmanager

class Cache:
    def __init__(self) -> None:
        
        super().__init__()

    def create_cache_dir(self):
        for dir in os.scandir():
            print(dir.name)
            if dir.is_dir() and dir.name == self.cache_dir:
                return True
        os.mkdir(self.cache_dir)    
        return True    

    #questa funzione crea un file nella cartella cache
    #il nome del file è composto dal nome fornito e dal timestamp unix
    #la timestamp è impostata all'inizio dell'ora corrente
    def create_file(self, file_name: str):
        now_timestring = time.strftime("%Y-%m-%d_%H")
        time_struct = time.strptime(now_timestring, "%Y-%m-%d_%H")
        file_unix_timestamp = str(int(time.mktime(time_struct)))
        file_name = f"{file_name}_{file_unix_timestamp}.json"
        #crea il file
        
        with open(os.path.join(self.cache_dir, file_name), "x") as f:
            pass
        print("file cr")


    #ritorna  tutti i files con il prefix fornito 
    #se il file è stato creato nell'intervallo di tempo fornito
    def get_files(self,prefix, time_slice:int = 3600) -> list:
        for file in os.scandir(self.cache_dir):
            if file.is_file():
                file_name = file.name
                #print(file_name)

                if file_name.startswith(prefix):
                    file_unix_timestamp = int(file_name.removeprefix(f"{prefix}_").removesuffix(".json"))
                    now_unix_timestamp = int(time.time())
                    if now_unix_timestamp - file_unix_timestamp < time_slice:
                        yield file_name

    #controlla se esiste un file con il prefix fornito
    # nell'intervallo di tempo fornito
    #se non esiste ne crea uno
    def check_users_cache(self,prefix, time_slice: int =  3600) ->bool:
        #si può avere al massimo un file della cache ogni ora
        #time_slice max 3600
        time_slice = time_slice if time_slice > 3600 else 3600 
        
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
            self.create_file(prefix)
            
        else:
            for file in self.get_files(prefix, time_slice):
                if file:
                    print(file)
                    print("file ex")
                    return True
            self.create_file(prefix)
     
    def read_cache(self, prefix, time_slice:int = 3600):
        #ritorna tutti gli item nel file della cache con il prefix fornito
        #nell intervallo di tempo fornito
        #si può avere al massimo un file della cache ogni ora
        #time_slice max 3600
        time_slice = time_slice if time_slice > 3600 else 3600 
        for file in self.get_files(prefix,time_slice):
            with open((os.path.join(self.cache_dir, file)), "r+") as cache_file:
                #apre i file della cache e ritorna gli item
                for user in json.load (cache_file):
                    yield user
    
    #serve per la gestione della lettura dei file

    def check_cache_file(self, prefix, time_slice:int = 3600):

        time_slice = time_slice if time_slice > 3600 else 3600
        newest_file = [file for file in self.get_files(prefix,time_slice)]
        #prende il nome del file più recente
        if newest_file:
            newest_file.sort()
            newest_file = newest_file[0]
        else:
            #se non esiste ne crea uno
            self.create_file(prefix)
            
            newest_file = [file for file in self.get_files(prefix,time_slice)]
            newest_file.sort()
            print(newest_file)
            newest_file = newest_file[0]
        print(newest_file)
        #salva la timestamp del file
        self.read_cache_timestamp = int(newest_file.removeprefix(f"{prefix}_").removesuffix(".json"))
        #apre il file
        read_cache_file = open((os.path.join(self.cache_dir, newest_file)), "r", encoding='utf-8')
        read_cache_file_text = read_cache_file.read()
        print(read_cache_file_text)

        #la libreria json ritorna un errore se il file è vuoto

        #se non è vuoto carica gli item
        #e li salva in un set
        if len(read_cache_file_text) > 0:
            print(read_cache_file_text)
            self.cache_items = json.loads(read_cache_file_text)
            self.cache_items = set(self.cache_items)
            print("carico dal vecchio file")

        else:
        #se è vutoto crea un set vuoto
            print("nuovo file")
            self.cache_items = set()

        read_cache_file.close()
        self.cache_file = open((os.path.join(self.cache_dir, newest_file)), "w", encoding='utf-8')

    def append_item(self, prefix, time_slice, item):
        
        #controlla con l'intervallo di tempo
        #se il file non è scaduto
        if (int(time.time()) - self.read_cache_timestamp) > time_slice:   
            #se è scaduto ne crea uno nuovo
            if self.cache_items:
                self.cache_items = None
            if self.cache_file:
                self.cache_file.close()
            self.check_cache_file(prefix, time_slice)
        
        #aggiunge l'item al set
        self.cache_items.add(item)
        print(list(self.cache_items))
        
        #riscrive il file con il set aggiornato
        self.cache_file.seek(0)
        json.dump(list(self.cache_items), self.cache_file)
        

    @contextmanager
    def edit_cache(self, prefix, time_slice:int = 3600):
        #si può avere al massimo un file della cache ogni ora
        #time_slice max 3600
        time_slice = time_slice if time_slice > 3600 else 3600
        
        #controlla se esiste un file con il prefix fornito
        #e lo carica
        self.check_cache_file(prefix, time_slice)
        
        try:
            
            #ritorna una funziona a cui passare l'item da aggiungere al file
            yield lambda item: self.append_item(prefix, time_slice, item)

        finally:
            #quando usciamo dal context manager chiude il file
            if self.cache_items:
                self.cache_items = None
            if self.cache_file:
                self.cache_file.close()

    def export_session_cookies(self,filename):
        with open(filename, "w") as f:
            json.dump(self.session_cookies, f)
        return True

    def load_session_cookies(self,filename):
        with open(filename, "r") as f:
            self.session_cookies = json.load(f)
        return True
    
    def loads_session_cookies(self,cookies):
        if cookies["sessionid"] and cookies["csrftoken"]:
            self.session_cookies = cookies
            return True
        else:
            return False