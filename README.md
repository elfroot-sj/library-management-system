# Library Management System – Istruzioni di installazione

Questa guida spiega come configurare l'ambiente di sviluppo del progetto.

Tutti i comandi di installazione devono essere eseguiti **dopo aver attivato l'ambiente virtuale**. In caso contrario, i pacchetti verranno installati a livello di sistema.

## 1. Creare un ambiente virtuale

```bash
python3 -m venv .venv
```

## 2. Attivare l'ambiente virtuale

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

Dopo l'attivazione, il terminale mostrerà il prefisso `(.venv)` all'inizio della riga, indicando che l'ambiente virtuale è attivo.

Se PowerShell blocca l'esecuzione degli script, eseguire una volta il seguente comando:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Uscire dall'ambiente virtuale

Per disattivare l'ambiente virtuale:

```bash
deactivate
```

Dopo questo comando il prefisso `(.venv)` scomparirà dal terminale, indicando che si è tornati all'ambiente Python di sistema.

## 3. Aggiornare pip

Con l'ambiente virtuale attivo, aggiornare `pip`:

```bash
pip install --upgrade pip
```

## 4. Installare le dipendenze di produzione

```bash
pip install -r requirements.txt
```

## 5. Installare le dipendenze di sviluppo

```bash
pip install -r requirements_dev.txt
```

## 6. Verificare l'installazione

Per controllare che i pacchetti siano stati installati correttamente:

```bash
pip list
```

## Estensioni consigliate per Visual Studio Code

- Python
- Pylance
- Python Debugger
- Python Environments
- SQLite Viewer