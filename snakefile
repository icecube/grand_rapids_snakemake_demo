OUTDIR = "outputs"
DATASETS = range(2)
XSECS =["csms", "csms_scaled"]
ICE_ABSS = [0.9, 1, 1.1]
ICE_SCAS = [0.9, 1, 1.1]

rule nugen:
    output: os.path.join(OUTDIR, "nugen_{dataset_id,\d+}_{xsec}.i3") 
    shell: "python run_nugen.py --seed {wildcards.dataset_id} --outfile {output}"
    

rule photon_prop:
    input: rules.nugen.output
    output: os.path.join(OUTDIR, "photon_prop_{dataset_id,\d+}_{xsec}_abs_{ice_abs}_sca_{ice_sca}.i3")
    shell: "python run_photon_prop.py --seed {wildcards.dataset_id} --abs {wildcards.ice_abs} --sca {wildcards.ice_sca} --infile {input} --outfile {output}"
    

rule proc_finallevel:
    input: rules.photon_prop.output
    output: os.path.join(OUTDIR, "finallevel_{dataset_id,\d+}_{xsec}_abs_{ice_abs}_sca_{ice_sca}.i3")
    shell: "python run_proc_fl.py --seed {wildcards.dataset_id} --infile {input} --outfile {output}"
    

rule aggregate_hdf:
    input: expand(os.path.join(OUTDIR, "finallevel_{dataset_id}_{{xsec}}_abs_{{ice_abs}}_sca_{{ice_sca}}.i3"), dataset_id=DATASETS)
    output:  os.path.join(OUTDIR, "combined_{xsec}_abs_{ice_abs}_sca_{ice_sca}.hdf")
    shell: "python run_agg_fl.py --infiles {input} --outfile {output}"
    

rule plot:
    input: expand(os.path.join(OUTDIR, "combined_{xsec}_abs_{ice_abs}_sca_{ice_sca}.hdf"), xsec=XSECS, ice_abs=ICE_ABSS, ice_sca=ICE_SCAS)
    output: os.path.join(OUTDIR, "plot.png")
    shell: "python run_plot.py --infiles {input} --outfile {output}"
    

