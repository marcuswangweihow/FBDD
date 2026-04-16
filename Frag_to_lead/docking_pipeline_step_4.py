print(f"\nStep 4: Run docking...")
#==================================================================
# Start docking ligands
#==================================================================
successful_all = []
failed_all = []

for item in config_files:

    config_file = item["config_file"]
    cavity_id = item["cavity_id"]
    snapshot = item["receptor_pdbqt"]

    grid_out_dir = os.path.join(
        out_dir,
        f"snap_{os.path.basename(snapshot).replace('.pdb','')}_grid_{cavity_id}"
    )

    success, failed = run_vina_docking(
        ligand_files=ligand_pdbqt_files,
        config_file=config_file,
        out_dir=grid_out_dir,
        cavity_id=cavity_id
    )

    successful_all.extend(success)
    failed_all.extend(failed)

print("Total successful:", len(successful_all))
print("Total failed:", len(failed_all))

#==================================================================
# Save to metadata
#==================================================================
docking_metadata["docking_summary"] = {
    "n_successful": len(successful_all),
    "n_failed": len(failed_all),
    "n_total": len(successful_all) + len(failed_all)
}

docking_metadata["successful_docking"] = successful_all
docking_metadata["failed_docking"] = failed_all

docking_metadata_file = os.path.join(docking_run_dir, f"docking_metadata.json")
with open(docking_metadata_file, "w") as f:
    json.dump(docking_metadata, f, indent=4, default=numpy_json_default)

print(f"docking_metadata saved to: {docking_metadata_file}")

print(f"\nStep 4 completed")