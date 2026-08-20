import os
import os.path as op
import shutil
import tempfile

from settings import load_config


def backup_save(config):
    backup_directory = op.join(config["backup_directory"])
    backup_directory_exists = op.isdir(backup_directory)

    stoneshard_directory = config["stoneshard_directory"]
    stoneshard_directory_exists = op.isdir(stoneshard_directory)

    print("----------- [Backup_Save]: W O R K I N G ----------")
    print("---------------------------------------------------\n")
    if not backup_directory_exists:
        os.mkdir(backup_directory)
        backup_directory_exists = op.isdir(backup_directory)
        print(f"-- [Backup_Save]: Creating A Backup Folder In \n\n{backup_directory}")
        print("---------------------------------------------------")

    if not stoneshard_directory_exists:
        print(
            f"-- [Backup_Save]: The Stoneshard Directory\n\n{stoneshard_directory}\n\nDoesn't Exist --"
        )
        print("---------------------------------------------------")
        return

    if len(os.listdir(stoneshard_directory)) != 3:
        print(
            f"-- [Backup_Save]: The Folder\n\n{stoneshard_directory}\n\nMust Have 3 Files Inside It --"
        )
        print("---------------------------------------------------")
        return

    if backup_directory_exists:
        stone_shard_number_of_files = len(os.listdir(stoneshard_directory))
        if stoneshard_directory_exists and stone_shard_number_of_files == 3:
            stone_shard_files = os.listdir(stoneshard_directory)

            # Stage the new save in a temporary folder first. The existing backup
            # is left completely untouched until every file has copied, so a copy
            # that fails part way through (the game often still holds the save open
            # right after "Save and Exit") can never leave the user with no backup.
            backup_directory_normalized = op.normpath(backup_directory)
            backup_parent = op.dirname(backup_directory_normalized)
            temp_directory = tempfile.mkdtemp(prefix=".exitsave_tmp_", dir=backup_parent)
            try:
                for file in stone_shard_files:
                    shutil.copy(stoneshard_directory + "/" + file, temp_directory)

                # Every file copied successfully. Only now do we swap the staged
                # copy in for the old backup: move the old backup aside, move the
                # new one into place, then delete the old one. Each move is atomic,
                # and if the second move fails we roll the old backup back.
                old_directory = temp_directory + "_old"
                os.replace(backup_directory_normalized, old_directory)
                try:
                    os.replace(temp_directory, backup_directory_normalized)
                except Exception:
                    os.replace(old_directory, backup_directory_normalized)
                    raise
                shutil.rmtree(old_directory, ignore_errors=True)
            except Exception:
                shutil.rmtree(temp_directory, ignore_errors=True)
                raise

            print(
                f"-- [Backup_Save]: Copied Files From:\n\n{stoneshard_directory}\n\n----------------------- To ------------------------\n\n{backup_directory}\n"
            )
            print("---------------------------------------------------")
            print("----------- [Backup_Save]: F I N I S H E D --------")
            print("---------------------------------------------------")


def main():
    config = load_config("config.json")
    backup_save(config)


if __name__ == "__main__":
    main()
