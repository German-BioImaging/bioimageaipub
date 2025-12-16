---
license: cc
language:
- en
tags:
- 3D
- Bioimaging
- Cancer
- Medical
- Molecule
- Drug
pretty_name: Chemical-genetic interaction map of small molecules in cancer
size_categories:
- 10M<n<100M
---

# A chemical-genetic interaction map of small molecules using high-throughput imaging in cancer cells

<!-- Provide a quick summary of the dataset. -->

Bioimages collection of a *high-content drug screening dataset for cancer*.

## Dataset Details

### Dataset Description

<!-- Provide a longer summary of what this dataset is. -->

We used high-content screening and image analysis to measure effects of 1280 pharmacologically active compounds on complex phenotypes in isogenic cancer cell lines which harbor activating or inactivating mutations in key oncogenic signaling pathways. Using multiparametric chemical-genetic interaction analysis, we measured 300,000 drug-gene-phenotype interactions and observed phenotypic gene-drug interactions for more than 193 compounds, with many affecting phenotypes other than cell growth.


- **Curated by:** [University of Dundee]
- **Funded by [optional]:** [BBSRC (Ref: BB/M018423/1), 688945 (Euro-BioImaging Prep Phase II), 653493 (Global BioImaging Project), 654248 (CORBEL), Wellcome Trust (Ref: 212962/Z/18/Z)]
- **Shared by [optional]:** [Stefan Dvoretskii (stefan.dvoretskii@dkfz-heidelberg.de)]
- **License:** [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

### Dataset Sources [optional]

<!-- Provide the basic links for the dataset. -->

- **Repository:** [IDR](https://idr.openmicroscopy.org/study/idr0017/)
- **Paper [optional]:** [A chemical-genetic interaction map of small molecules using high-throughput imaging in cancer cells](https://pubmed.ncbi.nlm.nih.gov/26700849/)

## Uses

<!-- Address questions around how the dataset is intended to be used. -->
Machine Learning pipelines for Bioimaging, drug screening data.

## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

Dataset is structured in [High-Content-Screening structure](https://docs.openmicroscopy.org/ome-model/5.5.7/developers/screen-plate-well.html) of OMERO. 
Images are **16-bit PNG** converted from OME-Zarr. **NB!: be aware of automatic 8-bit conversion by image tools, e.g. OpenCV!**

Metadata is provided in the tabular format (CSV) as well as JSON-LD objects.

## Dataset Creation

### Curation Rationale

Bioimaging and drug screening is cool, and HuggingFace lacks that!

### Source Data

[More information on drugs](http://dedomena.embl.de/PGPC/)

#### Data Collection and Processing

[Data collection overview](http://dedomena.embl.de/PGPC/)

#### Who are the source data producers?

Breinig M, Klein FA, Huber W, Boutros M

### Annotations [optional]

[Annotation files on Github](https://github.com/IDR/idr0017-breinig-drugscreen/tree/c4d21db7639899c73d1aedfba08b3f4ce71f88b1/screenA)

#### Annotation process

https://idr.openmicroscopy.org/about/screens.html

#### Who are the annotators?

IDR staff and original scientists

#### Personal and Sensitive Information

<!-- State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). If efforts were made to anonymize the data, describe the anonymization process. -->

No human PII / PHI has been noticed in the samples.

## Bias, Risks, and Limitations

Experiments could have contained errors / artifacts. Please refer to the original paper for more details.

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

**NB!: be aware of automatic 8-bit conversion by image tools, e.g. OpenCV!**

Original Zarr files contain a better resolution / additional lazy loading capabilities.

## Citation 
<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

@article{breinig2015chemical,
  title={A chemical--genetic interaction map of small molecules using high-throughput imaging in cancer cells},
  author={Breinig, Marco and Klein, Felix A and Huber, Wolfgang and Boutros, Michael},
  journal={Molecular systems biology},
  volume={11},
  number={12},
  pages={846},
  year={2015}
}
**APA:**

Breinig, M., Klein, F. A., Huber, W., & Boutros, M. (2015). A chemical–genetic interaction map of small molecules using high‐throughput imaging in cancer cells. Molecular systems biology, 11(12), 846.

## Glossary 
<!-- If relevant, include terms and calculations in this section that can help readers understand the dataset or dataset card. -->

[IDR glossary Google doc](https://docs.google.com/spreadsheets/d/1S9of23dD8vY1QUv90RV_-Ugu0h6yTeNobuj92-OoSl8/)

## More Information 

[IDR annotation](https://idr.openmicroscopy.org/study/idr0017/)


## Dataset Card Contact

[Stefan Dvoretskii](https://steved.netlify.app/)