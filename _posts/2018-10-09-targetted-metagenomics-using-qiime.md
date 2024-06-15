---
layout: post
title: Targetted 16S Metagenomic Analysis using Qiime
categories: [blog]
tags: [qiime, 16s, metagenomics, bioinformatics]
---

This was from a workshop I have given in the lab, but could be used as a guide for future analysis as well.*

## Background

Metagenomics involves the study of genomes found in the environment. Some microbes are difficult to culture in the laboratory, limiting the acquisition of data and study of genes in these organisms. Metagenomics involves sequencing and analyzing genomes of different organisms directly, without culturing and isolation, producing an unbiased profile of the community in a sample. Unlike whole genome analysis, metagenomic analysis is challenging in that the diversity of genomes in the sample produce redundancy of sequences between closely related community of microbes. In addition, the presence of multiple genomes in one sample complicates assembly, annotation, and the interpretation of data.

Targetted metagenomics aims to sequence and analyze only a portion of a genome or set(s) of genes from a given environmental sample. On the otherhad, shotgun sequencing involves indescriminate sequencing of DNA. This exercise covers basic steps in processing 16s rRNA targetted metagenomic sequences. 16s rRNA is one of the widely used genetic markers to profile bacterial communities.

<!--more-->

## Tools

QIIME version 1.9.1 [^1] [^2]

QIIME uses external tools in some of its modules. Please see [http://qiime.org](http://qiime.org) for a list of QIIME dependencies and their corresponding citations.

## Setting up
QIIME is an open-source software available at [http://qiime.org](http://qiime.org).  To install, simply run:

```bash
$ pip install qiime
```

Additional setting up include the following. Note that this is a non-exhaustive list and specifics would depend on the configurations of the machine you're using, the network, as well as the specific QIIME modules you are going to run, etc:


1. Download the `uchime` binary [here](https://drive5.com/uchime/uchime_download.html). Rename, copy, or link it as `uchime61`. Put the location of the binary in your `PATH` by either writing it in `.bashrc` or linking it in `/bin` or `/usr/local/bin`.

2. Make sure you have a copy of emperor or download it using 
```bash
$ sudo pip install emperor
````

3. If you have older versions of the Python module `numpy`, upgrade it using:
```bash
$ pip install -U numpy
```

4. QIIME works using older versions of `matplotlib`. To download specific versions of a Python module, e.g. matplotlib version 1.4.3:
```bash
$ pip install matplotlib==1.4.3
```

5. Set up `matplotlibrc`: 
```bash 
$ vi .config/matplotlib/matplotlibrc
```

    Go to `INSERT` mode by pressing `i` in your keyboard, then write the following:
    
    ```bash
    backend: agg
    ```
    This prevents matplotlib from using interactive mode when outputing figures. Save your edits by pressing `Esc` in your keyboard, and writing `:wq`.

6. Lastly, you also need to copy the QIIME config file to your home directory:
```bash
$ cat /etc/qiime/qiime_config > ~/.qiime_config
```


## Dowload databases

The following databases will be used for chimera searching and operational taxonomic units (OTU) picking:

1. Ribosomal Database Project (RDP) Gold sequences [^3], which can be downloaded at [here](http://drive5.com/uchime/rdp_gold.fa).
2. The Greengenes database [^4] which can be downloaded [here](http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz). Unpack the sequences before using, e.g.:
```bash
tar -xvzf gg_otus_4feb2011.tgz
```

## Organize (output) data into directories
Create directories where the resulting files will be written to. This is a good practice for organizing your data, intermediate files, and results. An example of commands to do this are as follows:

```bash
$ mkdir -p outputs/{01_multiple_join_paired_ends, \
           02_split_libraries_fastq, \
           03_identify_chimeric_seqs,04_filter_fasta, \
           05_pick_open_reference_otus, \
           06_summarize_taxa_through_plots,07_alpha_rarefaction, \
           08_biom_summarize_table, \
           09_alphadiversity,10_betadiversity}
$ mkdir outputs/04_filter_fasta/{data1,data2,merged}
$ mkdir outputs/08_biom_summarize_table/{data1,data2,merged}
```

## Sample workflow
This workflow uses 16s rRNA metagenomic reads, the QIIME modules, and the Linux commandline interface. It is assumed that you have a working knowledge of basic Linux commands.

1. Always refer to figure below for each of the steps.
2. For alpha diversity workflow only, do  **Step 1**- **Step 9**.
3. For beta diversity workflow only, do  **Step 1** - **Step 4**, and continue to **Step 10** - **Step 15**.

![Workflow]({{ site.url }}/assets/images/qiime-workflow.png){: width="700px"}

## Instructions

The input files are in FASTQ format inside the `data` directory.

1. Assemble forward and reverse reads into longer contigs or sequences.

    ```bash
    $ multiple_join_paired_ends.py -i data -o outputs/01_multiple_join_paired_ends
    ```
    The command above will produce FASTQ sequences with filename `fastqjoin.join.fastq` in the directory specified in the command. You may check if you have generated such file using `less` or `ls -l`.

2. Filter sequences by quality, and label each sequence with a "sample ID".

    ```bash
    $ split_libraries_fastq.py -i outputs/01_multiple_join_paired_ends/data1_R1_L001/fastqjoin.join.fastq -o outputs/02_split_libraries_fastq/data1 -q 19 --barcode_type 'not-barcoded' --sample_ids data1
    $ split_libraries_fastq.py -i outputs/01_multiple_join_paired_ends/data2_R1_L001/fastqjoin.join.fastq -o outputs/02_split_libraries_fastq/data2 -q 19 --barcode_type 'not-barcoded' --sample_ids data2
    ```

    This will produce sequences in FASTA format with filename `seqs.fna`. Each of the sequences inside `seqs.fna` should have a FASTA header starting with the specified string in the `--sample_ids` flag in the command, e.g. `data1_filename_0`. Check if you have a similar label using the Linux command `less`.
    Note: If possible, do not put non-alphanumeric characters such as "_" as your sample ID, as this may result in errors in succeeding steps. 

3. Identify chimeric sequences by comparing the assembled sequences from **Step 2** to sequences from the RDP Gold database.
    ```bash
    $ identify_chimeric_seqs.py -m usearch61 -i outputs/02_split_libraries_fastq/data1/seqs.fna -r /databases/rdp_gold/rdp_gold.fa -o outputs/03_identify_chimeric_seqs/data1
    $ identify_chimeric_seqs.py -m usearch61 -i outputs/02_split_libraries_fastq/data2/seqs.fna -r /databases/rdp_gold/rdp_gold.fa -o outputs/03_identify_chimeric_seqs/data2
    ```

    This step produces many files, most important of which is `chimeras.txt` which contains the names of sequences tagged to be chimeric. Check if you were able to generate such file.

4. Filter out sequences with chimera.
    ```bash
    $ filter_fasta.py -f outputs/02_split_libraries_fastq/data1/seqs.fna -o outputs/04_filter_fasta/data1/seqs_chimera_filtered.fna -s outputs/03_identify_chimeric_seqs/data1/chimeras.txt -n
    $ filter_fasta.py -f outputs/02_split_libraries_fastq/data2/seqs.fna -o outputs/04_filter_fasta/data2/seqs_chimera_filtered.fna -s outputs/03_identify_chimeric_seqs/data2/chimeras.txt -n
    ```

    The `-n` (negated) flag indicates that the supplied sequences via the flag `-s` must be removed.

5. Pick operational taxonomic units or OTUs from the sequences. First, create a paramaters file for the tool, by using `vi`. Press `i` to go into `INSERT MODE` then type the following:
    ```bash
    $ vi params.txt
    ```
    E.g.
    ```bash
    pick_otus:enable_rev_strand_match True
    plot_taxa_summary:chart_type pie,bar
    ```

    This file specifies other parameters for the OTU picking command in the first line in the format `<tool>:<parameter> value`. In addition, the second line specifies output formats for the next tool (`summarize_taxa_through_plots.py`).

    Press `Esc` on the keyboard, then type `:wq` and hit enter to save and quit. Execute the following commands to start OTU picking.

    ```bash
    $ pick_open_reference_otus.py -i outputs/04_filter_fasta/data1/seqs_chimera_filtered.fna -o outputs/05_pick_open_reference_otus/data1 -p params.txt -r /databases/gg_otus_4feb2011/rep_set/gg_99_otus_4feb2011.fasta --parallel --jobs_to_start=10
    $ pick_open_reference_otus.py -i outputs/04_filter_fasta/data2/seqs_chimera_filtered.fna -o outputs/05_pick_open_reference_otus/data2 -p params.txt -r /databases/gg_otus_4feb2011/rep_set/gg_99_otus_4feb2011.fasta --parallel --jobs_to_start=10
    ```

    The OTU picking script(s) of QIIME are in themselves a collection of tools and commands, see [this](http://qiime.org/scripts/pick_otus.html) for a description of these tools and steps. An "open reference" method of OTU picking, such as the one done in this step, is a combination of both referenced and *de novo* OTU picking.

    This step produces many files including binary files with extensions `biom` or Biological Observation Matrix. These files contain the OTU counts. More information about the `BIOM` format may be found [here](http://biom-format.org). 

    In addition, this step makes a phylogenetic tree of representative sequences of the OTUs identified `rep_set.tre`. Descriptions of relevant file outputs are in `index.html`.

6. Create summary plots of the OTUs found. First, create a mapping file containing details of the samples: sample ID, and description of each sample. Use the Linux command `vi`. Edit and save your file as in **Step 5**.

    ```bash
    $ vi mapping.tsv
    ```

    Write the following inside `mapping.tsv`. Note that the `.tsv` extension indicates that this is a tab-delimited file, i.e. a tab separates each value:

    ```bash
    #SampleID   Description
    data1   first_data
    data2   second_data_duplicate
    ```

    The mapping file (a.k.a the metadata mapping file) contains information about the sample. It contains information that may aid in the analysis of the samples e.g. sampling site, time points, barcodes, and primer used to amplify the sequences. `SampleID` and `Description` are among the important fields. 

    Note: To be useful and to avoid errors, use the *same* sample ID for each sample as supplied in the `--sample_ids` flag in **Step 2**. The mapping file will be used by other tools in this workflow.

    Run the following commands:

    ```bash
    $ summarize_taxa_through_plots.py -i outputs/05_pick_open_reference_otus/data1/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/06_summarize_taxa_through_plots/data1 -p params.txt -m mapping.tsv
    $ summarize_taxa_through_plots.py -i outputs/05_pick_open_reference_otus/data2/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/06_summarize_taxa_through_plots/data2 -p params.txt -m mapping.tsv
    ```

    This will generate bar plots and and pie charts of the taxonomic diversity found in the samples.

7. Create rarefaction curves.

    ```bash
    $ alpha_rarefaction.py -i outputs/05_pick_open_reference_otus/data1/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/07_alpha_rarefaction/data1 -m mapping.tsv -t outputs/05_pick_open_reference_otus/data1/rep_set.tre --parallel --jobs_to_start=10
    $ alpha_rarefaction.py -i outputs/05_pick_open_reference_otus/data2/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/07_alpha_rarefaction/data2 -m mapping.tsv -t outputs/05_pick_open_reference_otus/data2/rep_set.tre --parallel --jobs_to_start=10
    ```

    This step generates alpha rarefaction plots, as well as computes the alpha diversity metrics for each rarefied OTU table, and collate alpha diversity results.
    Chao 1 estimates true species diversity of a sample using an equtation based on the number of rare (singleton) and those seen twice (doubletons)[^5], while PD or phylogenetic diversity is also a measure of diversity based on the branch lengths of the phylogenetic tree generated[^6]. 

8. Create biom summary tables.

    ```bash
    $ biom summarize-table -i outputs/05_pick_open_reference_otus/data1/otu_table_mc2_w_tax_no_pynast_failures.biom  -o outputs/08_biom_summarize_table/data1/biom_summary.txt
    $ biom summarize-table -i outputs/05_pick_open_reference_otus/data2/otu_table_mc2_w_tax_no_pynast_failures.biom  -o outputs/08_biom_summarize_table/data2/biom_summary.txt
    ```

    This step outputs general summary metrics of the bioms generated by the OTU picking step. 

9. Compute alpha diversity or within-species diversity using the OTU table generated.

    ```bash
    $ alpha_diversity.py -i outputs/05_pick_open_reference_otus/data1/otu_table_mc2_w_tax_no_pynast_failures.biom -t outputs/05_pick_open_reference_otus/data1/rep_set.tre -o outputs/09_alphadiversity/data1.alpha_diversity
    $ alpha_diversity.py -i outputs/05_pick_open_reference_otus/data2/otu_table_mc2_w_tax_no_pynast_failures.biom -t outputs/05_pick_open_reference_otus/data2/rep_set.tre -o outputs/09_alphadiversity/data2.alpha_diversity
    ```

    *The following commands are applicable only for the beta-diversity workflow*. Similar descriptions of **Steps 11-14** can be found in **Steps 5-8**.

10. Concatenate cleaned sequences using the Linux command `cat`.

    ```bash
    $ cat outputs/04_filter_fasta/data1/seqs_chimera_filtered.fna outputs/04_filter_fasta/data2/seqs_chimera_filtered.fna > outputs/04_filter_fasta/merged/merged_seqs_chimera_filtered.fna
    ```

11. Pick OTUs in the combined datasets. First create a `params.txt` file as in **Step 5**.

    ```bash
    $ pick_open_reference_otus.py -i outputs/04_filter_fasta/merged/merged_seqs_chimera_filtered.fna -o outputs/05_pick_open_reference_otus/merged -p params.txt -r /databases/gg_otus_4feb2011/rep_set/gg_99_otus_4feb2011.fasta  --parallel --jobs_to_start=10
    ```

12. Plot the taxonomix diversity of the samples. First create a  `mapping.tsv` file as in **Step 6**.

    ```bash
    $ summarize_taxa_through_plots.py -i outputs/05_pick_open_reference_otus/merged/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/06_summarize_taxa_through_plots/merged -p params.txt -m mapping.tsv
    ```


13. Create rarefaction curves

    ```bash
    $ alpha_rarefaction.py -i outputs/05_pick_open_reference_otus/merged/otu_table_mc2_w_tax_no_pynast_failures.biom -o outputs/07_alpha_rarefaction/merged -m mapping.tsv -t outputs/05_pick_open_reference_otus/merged/rep_set.tre --parallel --jobs_to_start=10
    ```
```
14. Create biom summary tables

    ```bash
    $ biom summarize-table -i outputs/05_pick_open_reference_otus/merged/otu_table_mc2_w_tax_no_pynast_failures.biom  -o outputs/08_biom_summarize_table/merged/biom_summary.txt
```

15. Generate beta-diversity plots. Note that for this exercise, we will use other `biom` file and corresponding mapping file to illustrate how the tool can be ran because of the limitations of the tables generated from `data1` and `data2`.

    ```bash
    $ beta_diversity_through_plots.py -i subs/otu_table_mc2_w_tax_no_pynast_failures.biom -m subs/mapping.tsv -t subs/rep_set.tre -o outputs/10_betadiversity/merged --parallel --jobs_to_start=10
    ```

    Beta diversity is typically measured among samples from different sampling conditions or habitats. This step also generates interactive 3D Principal Coordinates of Analysis (PCoA) plots which groups points (samples) based on their distances.


## Directory structure
A sample directory structure containing the inputs and outputs can be found below.

Go to the working directory, e.g.  ```$ cd ~/qiime ```

```bash
data
----- data1_R1_L001.fastq *
----- data1_R2_L001.fastq *
----- data2_R1_L001.fastq *
----- data2_R2_L001.fastq *
outputs
----- 01_multiple_join_paired_ends
----- 02_split_libraries_fastq
----- 03_identify_chimeric_seqs
----- 04_filter_fasta
---------- data1
---------- data2
---------- merged
----- 05_pick_open_reference_otus
----- 06_summarize_taxa_through_plots
----- 07_alpha_rarefaction
----- 08_biom_summarize_table
---------- data1
---------- data2
---------- merged
----- 09_alphadiversity
----- 10_betadiversity
```



### References

[^1]: Kuczynski J, Stombaugh J, Walters WA, Gonzalez A, Caporaso JG, Knight R. (2011). Using QIIME to analyze 16S rRNA gene sequences from microbial communities. Current Protocols in Bioinformatics. Chapter 10:Unit 10.7.
[^2]: J Gregory Caporaso, Justin Kuczynski, Jesse Stombaugh, Kyle Bittinger, Frederic D Bushman, Elizabeth K Costello, Noah Fierer, Antonio Gonzalez Pena, Julia K Goodrich, Jeffrey I Gordon, Gavin A Huttley, Scott T Kelley, Dan Knights, Jeremy E Koenig, Ruth E Ley, Catherine A Lozupone, Daniel McDonald, Brian D Muegge, Meg Pirrung, Jens Reeder, Joel R Sevinsky, Peter J Turnbaugh, William A Walters, Jeremy Widmann, Tanya Yatsunenko, Jesse Zaneveld and Rob Knight. (2010). QIIME allows analysis of high-throughput community sequencing data. Nature Methods. doi:10.1038/nmeth.f.303
[^3]: Cole JR, Wang Q, Fish JA, Chai B, McGarrell DM, Sun Y, Brown CT, Porras-Alfaro A, Kuske CR, Tiedje JM. (2014). Ribosomal Database Project: data and tools for high throughput rRNA analysis. Nucleic Acids Research.42(Database issue):D633-42.
[^4]: DeSantis, T. Z., P. Hugenholtz, N. Larsen, M. Rojas, E. L. Brodie, K. Keller, T. Huber, D. Dalevi, P. Hu, and G. L. Andersen. 2006. Greengenes, a Chimera-Checked 16S rRNA Gene Database and Workbench Compatible with ARB. Appl Environ Microbiol 72:5069-72
[^5]: [http://palaeo-electronica.org/2011_1/238/estimate.htm](http://palaeo-electronica.org/2011_1/238/estimate.htm)
[^6]: [http://www.wernerlab.org/teaching/qiime/overview/e](http://www.wernerlab.org/teaching/qiime/overview/e)