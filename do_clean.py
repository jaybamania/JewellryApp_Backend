import os
import shutil
import time
import subprocess

start_time = time.time()
TERMINAL_WIDTH = shutil.get_terminal_size((80, 20)).columns


def main():
    print("Installing packages".center(TERMINAL_WIDTH, "-"))
    os.system("pip install -r requirements.txt")

    os.chdir('src')
    print("Deleting OLD DB file".center(TERMINAL_WIDTH, "-"))
    DB_FILE_PATH = os.path.join(os.getcwd(), "db.sqlite3")
    if os.path.exists(DB_FILE_PATH):
        os.remove(os.path.join(os.getcwd(), "db.sqlite3"))

    print("Removing Migrations".center(TERMINAL_WIDTH, "-"))
    if os.path.exists('user/migrations'):
        shutil.rmtree('user/migrations')
    if os.path.exists('product/migrations'):
        shutil.rmtree('product/migrations')

    print("Making User Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} makemigrations user".format(os.path.join(os.getcwd(), "manage.py")))

    print("Making Product Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} makemigrations product".format(os.path.join(os.getcwd(), "manage.py")))

    print("Migrating Migrations".center(TERMINAL_WIDTH, "-"))
    os.system("python {} migrate".format(os.path.join(os.getcwd(), "manage.py")))

    print("Creating Super User".center(TERMINAL_WIDTH, "-"))
    os.system("python {} createsuperuser --name SuperAdmin --email superadmin@gmail.com --mobile_no 1234".format(
        os.path.join(os.getcwd(), "manage.py")))

    # print("Runing Mcx Api Websocket".center(TERMINAL_WIDTH, "-"))
    # os.system("python {} mcx_api_websocket.py".format(os.path.join(os.path(os.getcwd()))))

    print("Adding groups")
    os.system("python add_group.py")

    print("Inserting Data".center(TERMINAL_WIDTH, "-"))
    os.chdir('../')
    os.system("python insert_data.py")

    # print("Starting Redis Server".center(TERMINAL_WIDTH, "-"))
    # os.chdir('Redis')
    # os.system("start {}\\redis-server.exe".format(os.path.join(os.getcwd())))
    # subprocess.call(["{}\\redis-server.exe".format(os.path.join(os.getcwd()))])

    # os.chdir("../")
    # print("Starting MCX APi Server".center(TERMINAL_WIDTH, "-"))
    # os.system(" start python {}mcx_api_websocket.py ".format(os.path.join(os.getcwd(), 'src\\MCX\\')))

    print("ALl DONE".center(TERMINAL_WIDTH, "-"))


if __name__ == "__main__":
    main()
    print("--- Completed in {} seconds ---".format(time.time() - start_time))
