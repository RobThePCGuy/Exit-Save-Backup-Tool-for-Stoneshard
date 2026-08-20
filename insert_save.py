import os
import os.path as op
import shutil

from settings import load_config


def insert_save(config):
    backup_directory = op.join(config["backup_directory"])
    backup_directory_exists = op.isdir(backup_directory)

    stoneshard_directory = config["stoneshard_directory"]
    stoneshard_directory_exists = op.isdir(stoneshard_directory)

    print("----------- [Insert_Save]: W O R K I N G ----------")
    print("---------------------------------------------------\n")
    if not stoneshard_directory_exists:
        os.mkdir(stoneshard_directory)
        print(
            f"-- [Insert_Save]: The Stoneshard exitsave_1 Folder Has Been Created In\n\n{stoneshard_directory}"
        )
        print("---------------------------------------------------")
        stoneshard_directory_exists = op.isdir(stoneshard_directory)

    if not backup_directory_exists:
        print(f"-- [Insert_Save]: The Backup Folder\n\n{backup_directory}\n\nDoesn't Exist")
        print("---------------------------------------------------")
        pass

    if stoneshard_directory_exists and backup_directory_exists:
        backup_files = os.listdir(backup_directory)

        # Make sure there is actually a usable backup before we touch the live
        # save. An empty (or incomplete) backup folder would otherwise be
        # reported as a successful restore while copying nothing.
        if len(backup_files) != 3:
            print(
                f"-- [Insert_Save]: The Backup Folder\n\n{backup_directory}\n\nMust Have 3 Files Inside It To Restore --"
            )
            print("---------------------------------------------------")
            return

        for file in backup_files:
            shutil.copy(backup_directory + "/" + file, stoneshard_directory)

        # Only report success once every file has actually copied.
        print(
            f"-- [Insert_Save]: Copied The Backup Exit Save From:\n\n{backup_directory}\n\n----------------------- To ------------------------\n\n{stoneshard_directory}\n"
        )
        print("---------------------------------------------------")
        print("----------- [Insert_Save]: F I N I S H E D --------")
        print("---------------------------------------------------")


def main():
    config = load_config("config.json")
    insert_save(config)


if __name__ == "__main__":
    main()
