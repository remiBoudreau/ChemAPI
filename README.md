<br />
<div align="center">

  <h3 align="center">Materials Project-PubChem Chemistry API</h3>

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

### GET /data/csv/{ids}

Write comprehensive chemical data for multiple IDs to csv.

#### Example:

```bash
GET /data/csv/mp-123456,mp-789012
```

Note that some of the endpoints the API calls from within its funcitons do not have the capabilities to handle a great deal of traffic, so try not to send too many requests at once.
