<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Materials Project-PubChem Chemistry API</h3>

  <p align="center">
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#usage">Endpoints</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

API that uses extract Chemical and Materials Science properties from the Materials Project Database and PubChem Database using Materials Project IDs. Endpoints can be used seperately or as a pipeline through the endpoint

```text
/data/{material_property_ids}.
```

### Properties that the API provides:

* Material Property ID
* Formula
* Volume (Å<sup>3</sup>)
* Density (g/cm<sup>3</sup>)
* Symmetry
* Band Gap (eV)
* Pubchem cID
* CAS Registry Number
* IUPAC Name
* Molecular Weight (g/mol)
* Canonical Smiles
* InChI
* InChIkey
* Hydrogen Bond Donors
* Hydrogen Bond Acceptors
* Rotatable Bonds

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get started, first clone the repository to your local machine: 

```bash
git clone https://github.com/remiBoudreau/ChemAPI.git
```

Install the dependencies by the following command in the root directory of the API:

```bash
pip install -r requirements.txt
```

Then, ensure that MP_API_KEY is defined in your envioronment. On Debian machines, you may do that by adding the following command to your $HOME/.bashrc file:

```bash
export MP_API_KEY=YOUR_API_KEY_HERE
source $HOME/.bashrc
```

If you don't have an Materials Project API Key, check out the [Materials Project API Page](https://next-gen.materialsproject.org/api) for instructions on obtaining one.

## Usage

To start the API server in development mode, use the uvicorn package:

```bash
uvicorn main:app --reload
```

To create a README.md file with information on the usage of the API, you can provide instructions on how to interact with each endpoint and include some usage examples. Here's a suggested README.md content:

## Endpoints

### GET /mpID/{ids}

Retrieve chemical data from the Materials Project using Materials Project IDs.

#### Example:

```bash
GET /mpID/mp-123456
```

### GET /formula/{formula}

Retrieve CAS Registry Number from a chemical formula.

#### Example:

```bash
GET /formula/H2O
```

### GET /cts/{casRegistryNumber}

Retrieve PubChem CID from a CAS Registry Number.

#### Example:

```bash
GET /cts/64-17-5
```

### GET /pubchemcID/{id}

Retrieve chemical data from PubChem using a PubChem CID.

#### Example:

```bash
GET /pubchemcID/12345
```

### GET /data/{ids}

Retrieve comprehensive chemical data for multiple IDs.

#### Example:

```bash
GET /data/mp-123456,mp-789012
```

Note that some of the endpoints the API calls from within its funcitons do not have the capabilities to handle a great deal of traffic, so try not to send too many requests at once.
