---
layout: post
title: Notes on setting up MAKER2
categories: [blog, bioinformatics]
tags: [maker2]
---

This is a quick reference for installing the parallel version of [Maker2](https://www.yandell-lab.org/software/maker.html). I wrote this a while back (about 3 years) but could be useful still. Some of the tools could have undergone major updates in that timeframe.

## Software
1. MAKER2 [link](http://www.yandell-lab.org/software/maker.html)
2. mpich2 [link](http://www.mpich.org/downloads/)
3. genemark (es/et) [link](http://exon.gatech.edu/Genemark/license_download.cgi)
4. tRNAScan [link](http://lowelab.ucsc.edu/tRNAscan-SE/)
5. ncbi-toolkit [link](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
5. augustus [link](http://bioinf.uni-greifswald.de/webaugustus/)

<!--more-->

If downloading RepBase with repeatmasker, register at site first [link](http://www.girinst.org/repbase/)

Will use GeneMark instead of FGENESH, and blast execs (NCBI toolkit) instead of WUBLAST

Also install GeneMark for prokaryotic (has exec `gmhmmp`) if annotating prokaryotic

Executables: `exonerate`, `formatdb`, and `blastall` must also be present, but installation not included here

## Installation
### mpich-3.2.tar.gz

Important to enable shared libraries, `gcc` is standard for Linux. Use `--prefix` to prevent installation in root dirs

```bash
tar -xvf mpich-3.2.tar.gz
cd mpich-3.2/
./configure --prefix=$PWD/execs --enable-sharedlibs=gcc
```
Continue with installation.
```bash
make
make install
```
Executables should be in `bin/execs`. Test using `./mpiexec -n 2 echo hello`
```
hello
hello
```
Source to `bashrc` so don't have to type the path later when MAKER2 asks.

### maker-2.31.8.tgz

```bash
tar -xvf maker-2.31.8.tgz
cd maker/src
perl Build.PL
## Y to mpi install
```
Install PERL dependencies
```bash
./Build installdeps
## Y to local install
```

Open file `vi locations`. Find path to Repbase for specific OS e.g. Linux , then change url to latest version, e.g.: 'http://www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/repeatmaskerlibraries-20150807.tar.gz' because the old one won't work with the username and password

Install SNAP and RepeatMasker, etc (alternatively just source them if they're already installed so MAKER2 will know)
```bash
./Build installexes
## enter username and password for RepBase
./Build status ## to see install status, should see OK, verified, enabled, etc
./Build install 
````
Executables should be in `maker/bin` , NOT `maker/src/bin`

### augustus-3.2.2.tar.g
```bash
tar -xvf augustus-3.2.2.tar.gz
cd apps/augustus-3.2.2
make
## make install if you're an admin
```
Source in `bashrc`

### gm_et_linux_64.tar.gz
```bash
tar -xvf gm_et_linux_64.tar.gz
cd gm_et_linux_64/gmes_petap
cp gm_key ~/.gm_key ## copy license to home
```
Source in `bashrc`

### tRNAscan-SE.tar.Z
```bash
tar -xvf tRNAscan-SE.tar.Z
cd tRNAscan-SE-1.23
```
Edit the `Makefile` using `vi Makefile`
```
BINDIR  = /home/mbr/apps/tRNAscan-SE-1.23/bin
LIBDIR  = /home/mbr/apps/tRNAscan-SE-1.23/lib/tRNAscan-SE
MANDIR  = /home/mbr/apps/tRNAscan-SE-1.23/man
```
Correct the getline error during compilation in Linux
```bash
perl -pi -e "s/getline/getline2/g" sqio.c
```
This changes all getline to getline2 since getline is an environmental variable in Linux

```bash
make
make install
```
Source in `bashrc`

### ncbi-blast-2.4.0+
Just unpack it, and test. Source in `bashrc`

### snoscan.tar.gz
```bash
tar -xvf snoscan.tar.gz
```
Build squid first
```bash
cd snoscan-0.9b/squid-1.5j
```
Set everything to squid dir using `vi Makefile`
```
SQUIDHOME  = $(PWD)/lib/squid
BINDIR     = $(PWD)/bin
SCRIPTDIR  = $(PWD)/scripts
MANDIR     = $(PWD)/man
```

Correct compile error (same as above)
```bash
perl -pi -e "s/getline/getline2/g" sqio.c
```
Install
```bash
make
make install 
cd ..
make
```
Source in `bashrc`

## Test MAKER2 installation
```bash
cd ~
mkdir maker
cd maker
cp -r /path/to/maker/data/ .
maker -CTL
```
Edit maker_opts.ctl
```
  genome=data/dpp_contig.fasta
  est=data/dpp_est.fasta
  protein=data/dpp_protein.fasta
```

Check paths in `maker_exe.ctl`, should have the expected paths of other tools, if not, source tools, or edit this file

No mpi
```bash
time maker
```

Will see this warning:
```
Argument "2.53_01" isn't numeric in numeric ge (>=) at /home/mbr/apps/maker/bin/../perl/lib/forks.pm line 1570.
```
This does not affect maker run as far as I can see.. time. Outputs in `dpp_contig.maker.output`, i.e. genome+"maker.output"
```
 real    1m11.850s
 user    1m33.228s
 sys     0m5.048s
```

With mpi `time mpiexec -n 5 maker -base=withMpi`
```
 real    0m30.808s
 user    0m52.076s
 sys     0m3.592s
```

## Output
```bash
cd withMpi.maker.output/
```
Generate `gff3` files
```bash
gff3_merge -n -d withMpi_master_datastore_index.log
```
Generate `fasta` annotation files
```bash
fasta_merge -d withMpi_master_datastore_index.log
```