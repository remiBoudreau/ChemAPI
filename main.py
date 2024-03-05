from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from mp_api.client import MPRester
import requests
import time
import csv
import os
from bs4 import BeautifulSoup
import json
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests only from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000", "http://127.0.0.1", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# API endpoint to retrieve chemical data from the Materials Project using Materials Project IDs
@app.get("/mpID/{ids}")
async def mpid(ids: str):
    """
    Retrieve chemical data from the Materials Project using Materials Project IDs.
    """
    logger.info(f"Materials Project ID: {ids}. Retrieving summary of chemicals with Materials Project IDs {ids}...")
    mp_summaries = []
    with MPRester(os.environ.get("MP_API_KEY")) as mpr:
        ids = ids.replace(" ", "").split(',')
        response = mpr.summary.search(material_ids=ids)
        for summary in response: 
            mp_summary = {}
            mp_summary['mp_id'] = str(summary.material_id) if summary.material_id else ""
            mp_summary['formula'] = str(summary.formula_pretty) if summary.formula_pretty else ""
            mp_summary['volume'] = str(summary.volume) if summary.volume else ""
            mp_summary['density'] = str(summary.density) if summary.density else ""
            mp_summary['symmetry'] = str(summary.symmetry.crystal_system) if summary.symmetry else ""
            mp_summary['band_gap'] = str(summary.band_gap) if summary.band_gap else ""
            mp_summaries.append(mp_summary)
    return mp_summaries

# API endpoint to retrieve CAS Registry Number from a chemical formula
@app.get("/formula/{formula}")
async def formula2casnumber(formula: str):
    """
    Retrieve CAS Registry Number from a chemical formula.
    """
    logger.info(f"Formula: {formula}. Retrieving CAS Registry Number from formula...")
    url = f"https://webbook.nist.gov/cgi/cbook.cgi?Formula={formula}&NoIon=on&Units=SI"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve CAS Registry Number for formula: {formula}")
    try:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the h1 tag with id "Top"
        h1_tag = soup.find('h1', id='Top')
        # Find the immediate sibling ul tag
        ul_tag = h1_tag.find_next_sibling('ul')
        # Get the third li element within the ul tag
        third_li = ul_tag.find_all('li')[2]
        # Extract text within the li tag but not within its children tags
        cas_text = third_li.get_text(strip=True)
        # Extract the CAS Registry Number
        cas_number = cas_text.split(':')[1].strip()
        logger.info(f"CAS Number for formula: {formula} is {cas_number}")
    except:
        logger.error(f"No CAS Registry Number found for formula: {formula}")
        cas_number = ""
    return cas_number

# API endpoint to retrieve PubChem CID from a CAS Registry Number
@app.get("/cts/{casRegistryNumber}")
async def cas2pubchemcid(casRegistryNumber: str):
    """
    Retrieve PubChem CID from a CAS Registry Number.
    """
    logger.info(f"CAS Registry Number: {casRegistryNumber}. Retrieving PubChem CID from CAS Registry Number...")
    url = f"https://cts.fiehnlab.ucdavis.edu/rest/convert/CAS/Pubchem%20CID/{casRegistryNumber}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"{url} responded with http code {response.status_code} for CAS Registry Number: {casRegistryNumber}")
    # Convert string representation of dictionary into dictionary
    cts_dict = json.loads(response.text)[0]
    # Extract the PubChem CID
    pubchem_cid = cts_dict.get("results", None)[0]
    if not pubchem_cid:
        logger.error(f"No PubChem CID found for CAS Registry Number: {casRegistryNumber}")
    return pubchem_cid

# API endpoint to retrieve chemical data from PubChem using a PubChem CID
@app.get("/pubchemcID/{ids}")
async def pubchem(ids: str):
    """
    Retrieve chemical data from PubChem using a PubChem CID.
    """
    logger.info(f"PubChem cIDs: {ids}. Retrieving data from PubChem...")
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/JSON?cid={ids}"
    if url[-1] == ',':
        url = url[:-1]
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve data from PubChem for PubChem cIDs: {ids}")
    return response.json()

# API endpoint to retrieve comprehensive chemical data for multiple IDs
@app.get("/data/{ids}")
async def get_comprehensive_data(ids: str):
    """
    Retrieve comprehensive chemical data for multiple IDs.
    """
    chem_dict = {
        "mp_id": [],
        "formula": [],
        "volume (A^3)": [],
        "density (g/cm^3)": [],
        "symmetry": [],
        "band_gap (eV)": [],
        "pubchem_cid": [],
        "cas_rn": [],
        "iupac_name": [],
        "molecular_weight (g/mol)": [],
        "canonical_smiles": [],
        "inchi": [],
        "inchikey": [],
        "hbd": [],
        "hba": [],
        "rb": [],
    }
    max_ids = 5
    ids_list = ids.split(',')
    if len(ids_list) > max_ids:
        raise HTTPException(status_code=400, detail=f"Too many IDs provided. Please provide no more than {max_ids} IDs.")

    pubchem_cids = []
    for mp_id in ids_list:
        mp_summaries = await mpid(mp_id)
        for mp_summary in mp_summaries:
            formula = mp_summary.get('formula')
            cas_number = await formula2casnumber(formula)
            if not cas_number:
                pubchem_cid = ""
            else:
                pubchem_cid = await cas2pubchemcid(cas_number)            

        chem_dict['mp_id'].append(str(mp_id))
        chem_dict['formula'].append(str(formula))
        chem_dict['volume (A^3)'].append(str(mp_summary.get('volume')))
        chem_dict['density (g/cm^3)'].append(str(mp_summary.get('density')))
        chem_dict['symmetry'].append(str(mp_summary.get('symmetry')))
        chem_dict['band_gap (eV)'].append(str(mp_summary.get('band_gap')))
        chem_dict['pubchem_cid'].append(str(pubchem_cid))
        chem_dict['cas_rn'].append(str(cas_number))
        pubchem_cids.append(str(pubchem_cid))  # Append PubChem CID for consistency
        time.sleep(1)  # Prevent too many API requests to prevent IP blocking
    pubchem_response = await pubchem(str(','.join(pubchem_cids)))
    # Initialize lists for PubChem CID-related properties with empty values
    for _ in range(len(ids_list)):
        chem_dict['iupac_name'].append('')
        chem_dict['molecular_weight (g/mol)'].append('')
        chem_dict['canonical_smiles'].append('')
        chem_dict['inchi'].append('')
        chem_dict['inchikey'].append('')
        chem_dict['hbd'].append('')
        chem_dict['hba'].append('')
        chem_dict['rb'].append('')

    for compound in pubchem_response["PC_Compounds"]:
        pubchem_cid = compound["id"]["id"]["cid"]
        try:
            index = chem_dict['pubchem_cid'].index(str(pubchem_cid))
        except ValueError:
            continue
        for prop in compound["props"]:
            if prop["urn"].get("label") == "IUPAC Name":
                chem_dict['iupac_name'][index] = prop["value"]["sval"]
            if prop["urn"].get("label") == "Molecular Weight":
                chem_dict['molecular_weight (g/mol)'][index] = prop["value"]["sval"]
            if prop["urn"].get("label") == "SMILES" and prop["urn"].get("name") == "Canonical":
                chem_dict['canonical_smiles'][index] = prop["value"]["sval"]
            if prop["urn"].get("label") == "InChI":
                chem_dict['inchi'][index] = prop["value"]["sval"]
            if prop["urn"].get("label") == "InChIKey":
                chem_dict['inchikey'][index] = prop["value"]["sval"]
            if prop["urn"].get("name") == "Hydrogen Bond Donor":
                chem_dict['hbd'][index] = prop["value"]["ival"]
            if prop["urn"].get("name") == "Hydrogen Bond Acceptor":
                chem_dict['hba'][index] = prop["value"]["ival"]
            if prop["urn"].get("label") == "Rotatable Bond":
                chem_dict['rb'][index] = prop["value"]["ival"]

    return chem_dict

@app.get("/help")
async def help():
    """
    Display API usage information.
    """
    message = """
    Welcome to the Chemical Data API!

    This API allows you to retrieve chemical data from various sources.

    Available Endpoints:
    - GET /mpID/{ids}: Retrieve chemical data from the Materials Project using Materials Project IDs.
    - GET /formula/{formula}: Retrieve CAS Registry Number from a chemical formula.
    - GET /cts/{casRegistryNumber}: Retrieve PubChem CID from a CAS Registry Number.
    - GET /pubchemcID/{id}: Retrieve chemical data from PubChem using a PubChem CID.
    - GET /data/{ids}: Retrieve comprehensive chemical data for multiple IDs.

    Usage Examples:
    - GET /mpID/mp-123456: Retrieve chemical data for Materials Project ID 'mp-123456'.
    - GET /formula/H2O: Retrieve CAS Registry Number for the chemical formula 'H2O'.
    - GET /cts/64-17-5: Retrieve PubChem CID for the CAS Registry Number '64-17-5'.
    - GET /pubchemcID/12345: Retrieve chemical data from PubChem for PubChem CID '12345'.
    - GET /data/mp-123456,mp-789012: Retrieve comprehensive chemical data for Materials Project IDs 'mp-123456' and 'mp-789012'.

    For more information, refer to the API documentation or contact support.
    """
    return message
