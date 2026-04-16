def run_vina_docking(
    ligand_files,
    config_file,
    out_dir,
    cavity_id,
    vina_executable="vina",
    log_file_path=None,
    print_every=200
):
    """
    Run AutoDock Vina docking for a list of ligand PDBQT files.
    """

    os.makedirs(out_dir, exist_ok=True)

    if log_file_path is None:
        log_file_path = os.path.join(out_dir, "docking_log.txt")

    total = len(ligand_files)

    print(f"Found {total} ligands to dock for cavity {cavity_id}.\n")

    failed_docking = []
    successful_docking = []

    with open(log_file_path, "w") as log_file:
        for idx, ligand_path in enumerate(ligand_files, start=1):

            ligand_name = os.path.basename(ligand_path)
            out_path = os.path.join(out_dir, f"docked_{ligand_name}")

            cmd = [
                vina_executable,
                "--config", config_file,
                "--ligand", ligand_path,
                "--out", out_path
            ]

            if idx % print_every == 0 or idx == 1 or idx == total:
                message = f"[{idx}/{total}] Docking {ligand_name} (cavity {cavity_id})..."
                print(message)
                log_file.write(message + "\n")

            try:
                subprocess.run(
                    cmd,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    check=True
                )

                successful_docking.append({
                    "cavity": cavity_id,
                    "ligand": ligand_name,
                    "out": out_path
                })

            except subprocess.CalledProcessError as e:
                error_message = f"Error docking {ligand_name}: {e}"
                print(error_message)
                log_file.write(error_message + "\n")

                failed_docking.append({
                    "cavity": cavity_id,
                    "ligand": ligand_name,
                    "error": str(e)
                })

    print(f"\nAll ligands docked for cavity {cavity_id}!")

    return successful_docking, failed_docking