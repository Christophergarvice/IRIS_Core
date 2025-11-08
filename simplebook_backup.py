import os, subprocess, datetime, zipfile, shutil

# Directories to include
PROJECT_DIR = os.path.expanduser("~/PycharmProjectsSimpleBook_Parser")
LOG_DIR = os.path.expanduser("~/SimpleBook_Logs")
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

def zip_logs():
    """Compress daily logs older than 3 days."""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=3)
    for f in os.listdir(LOG_DIR):
        if f.endswith(".txt"):
            date_part = f[:10]
            try:
                d = datetime.datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                continue........................................
            if d < cutoff:
                zfile = os.path.join(ARCHIVE_DIR, f"logs_until_{date_part}.zip")
                with zipfile.ZipFile(zfile, "a", zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(os.path.join(LOG_DIR, f), arcname=f)
                os.remove(os.path.join(LOG_DIR, f))

def git_backup():
    """Commit and push all changes to GitHub."""
    try:
        subprocess.run(["git", "-C", PROJECT_DIR, "add", "."], check=True)
        msg = f"Automated backup {datetime.datetime.now().isoformat(timespec='seconds')}"
        subprocess.run(["git", "-C", PROJECT_DIR, "commit", "-m", msg], check=True)
        subprocess.run(["git", "-C", PROJECT_DIR, "push"], check=True)
        print("Backup pushed to GitHub.")
    except subprocess.CalledProcessError:
        print("Git push failed. Check internet or credentials.")

def main():
    zip_logs()
    git_backup()

if __name__ == "__main__":
    main()