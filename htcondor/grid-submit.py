#!/usr/bin/env python3

import sys
import htcondor
from os import makedirs
from os.path import join
from uuid import uuid4

from snakemake.utils import read_job_properties


jobscript = sys.argv[1]
job_properties = read_job_properties(jobscript)

UUID = uuid4()  # random UUID
jobDir = "/scratch/chaack/condor_logs/{}_{}".format(job_properties["jobid"], UUID)
makedirs(jobDir, exist_ok=True)

sub = htcondor.Submit(
    {
        "executable": "/bin/bash",
        "arguments": jobscript,
        "max_retries": "5",
        "log": join(jobDir, "condor.log"),
        "output": join(jobDir, "condor.out"),
        "error": join(jobDir, "condor.err"),
        "getenv": "True",
        "request_cpus": str(job_properties["threads"]),
        "should_transfer_files": "True",
    }
)

request_memory = job_properties["resources"].get("mem_mb", None)
if request_memory is not None:
    sub["request_memory"] = str(request_memory)

request_disk = job_properties["resources"].get("disk_mb", None)
if request_disk is not None:
    sub["request_disk"] = str(request_disk)

schedd = htcondor.Schedd()
with schedd.transaction() as txn:
    clusterID = sub.queue(txn)

# print jobid for use in Snakemake
print("{}_{}_{}".format(job_properties["jobid"], UUID, clusterID))
