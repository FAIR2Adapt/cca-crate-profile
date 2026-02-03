---
layout: default
title: Home
---

# Climate Change Adaptation RO-Crate profile
{: .no_toc }

Fair2Adapt project uses RO-Crates for implementing and exchanging FAIR Digital Objects (FDOs) for Climate Change Adapttion (CCA) research, and defines the CCA RO-Crate profile to define the set of conventions, types and properties that one can minimally require and expect to be present in that subset of RO-Crates.

The CCA RO-Crates are a specialization of RO-Crate for packaging key common data and contextual entities used/produced during the research lifecycle in climate change adaptation domain. This includes all the metadata properties expected to be captured and exposed about these resources to enable FAIR discovery, access and reuse. 

---

## Table of Contents
{: .no_toc }

* TOC
{:toc}

---

## Introduction

The FAIR2Adapt is a multidisciplinary project geared towards transforming data into actionable knowledge to shape climate adaptation strategies. We adopt FAIR Digital Objects (FDOs) by using RO-Crate and other complementary technologies (like nanopublications, I-Adopt framework) and use tailored FDO services to build a collaborative, user-friendly FAIR and open data sharing framework. 

Rich case studies will co-develop FAIR Supporting Resources in alignment with the FAIRification framework and demonstrate the impact of FAIR and open data sharing on climate change adaptation, and strategically support the EU Mission’s objective of enhancing climate resilience in European regions and communities.

## Concepts

This section uses terminology from the RO-Crate 1.2 specification.

### Context
The Crate JSON-LD MUST be valid according to RO-Crate 1.2 and SHOULD use the RO-Crate 1.2 @context https://w3id.org/ro/crate/1.2/context

### Metadata File Descriptor
RO-Crates that are conforming to (or intending to conform to) cca profile **SHOULD** declare this using `conformsTo` on the [Root Data Entity](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity):

```json
{
    "@id": "./",
    "@type": "Dataset",
    "conformsTo": {
        "@id": "https://w3id.org/cc-crate-profile/0.9"
    }
}
```

## CCA-specific Entities/Requirements

### Prefixes used in semantic terms

| Prefix | Namespace IRI |
|---|---|
| adms | http://www.w3.org/ns/adms# |
| bibo | http://purl.org/ontology/bibo/ |
| citedcat | https://w3id.org/citedcat-ap/ |
| dcat | http://www.w3.org/ns/dcat# |
| dcso | https://w3id.org/dcso/ns/core# |
| dct | http://purl.org/dc/terms/ |
| dpv | https://w3id.org/dpv# |
| fabio | http://purl.org/spar/fabio/hasEmbargoDuration |
| foaf | http://xmlns.com/foaf/0.1/ |
| iadopt | https://w3id.org/iadopt/ont/ |
| rdfs | http://www.w3.org/2000/01/rdf-schema# |
| sosa | http://www.w3.org/ns/sosa/madeBySensor |
| tech | https://w3id.org/dpv/tech# |
| geodcat | http://data.europa.eu/930/ |
| schema | https://schema.org/ |
| cca | https://w3id.org/ro/terms/cca/ |


---

### MVP
This entity defines a Minimal Viable Product (MVP) along with the related metadata fields enabling its findability. 

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **MVP** | class | should | schema:Product | Defines the MVP entity in the metadata model |
| variable | object property | should | schema:variableMeasured | variables used in the models to produce the output |
| depth level | data property | should | schema:depth | Depth level of the analysis |
| time range | data property | should | schema:temporalCoverage | Time range of the data icluded in the output |
| spatial extent | object property | should | schema:spatialCoverage | Spatial extent of the data icluded in the output (DGGS id/bbox) |
| scenario/run id | data property | should | cca:scenarioId | Scenario/run id of the model output |
| grid resolution | data property | should | geodcat:spatialResolutionAsText | Grid resolution of the model output |
| licence | object property | should | schema:license | License of the output |
| version DOI | data property | should | schema:identifier | DOI of the output |
| provenance URL | object property | should | dct:provenance | Provenance URL of the model output |

### Variable

This entity defines a variable or observed property represented according to the I-ADOPT model, along with the related metadata fields enabling its findability. 

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Variable** | class | may | iadopt:Variable | Defines the a variable or observed property entity represented according to the I-ADOPT model in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name (e.g., number, text, date) |
| url | data property | may | schema:url | Captures the literal value for URL (e.g., number, text, date) |

### Project-Level Metadata Fields

This section defines a conceptual entity representing a related project along with the related metadata fields enabling its findability. 

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Project** | class | may | schema:Project | Defines the Project entity in the metadata model. |
| data management plan (DMP) reference | object property | may | cca:dmp_id | Identifies data managers for each type of data |
| expected deliverables | data property | may | cca:expectedDeliverable | Lists planned outputs with timeline codes |
| reused data | object property | may | cca:reusedData | Identifies external data sources |
| general WP program | data property | may | cca:generalWPProgram | Overview of data collection activities |

### Network Metadata Structure

This section defines the conceptual entities representing a related network along with the related metadata fields enabling its findability. 

#### Network

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Network** | class | may | cca:Network | Defines the Network contextual entity in the metadata model |
| has network | object property | may | cca:hasNetwork | Defines a relationship with a Network contextual entity |
| network manager | object property | may | cca:networkManager | Defines a relationship for Network Manager between metadata entities |
| name | data property | should | schema:name | Network/SNO name |
| data manager | object property| may | citedcat:dataManager geodcat:custodian | Data responsible persons |
| scientific coordination | object property | may | geodcat:principalInvestigator | Scientific coordination lead |
| partners | object property | may | schema:member | Partner organizations |
| labelling | data property | may | rdfs:label | Labeling year (first and last) |
| ILICO integration year | data property | may | cca:IlicoIntegrationYear | ILICO integration year |
| scientific issues | data property | may | cca:scientificIssues | Research questions and objectives |
| grants | object property | may | schema:funding or schema:funder (if grant is not needed/known) | Funding organizations |
| network costs | data property | may | cca:averageNetworkCost | Average infrastructure costs |
| data costs | data property | may | cca:averageDataCost | Average data costs |

#### Dataset

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Dataset** | class | may |  schema:Dataset | Defines the Dataset entity in the metadata model. |
| data creation/collection | object property | may | schema:dataset | Defines a relationship for Data Creation/Collection between metadata entities. |
| data creation manager | object property | should | citedcat:dataCollector | Data creation/collection responsible |
| type | data property | may | dct:type | Type of data (collected/produced) |
| origin | data property | should | dct:source | Data source type (observations/experimental/simulations/derived) |
| nature | data property | should | cca:dataNature | Data nature (textual/numerical/audiovisual/modeled/discipline-specific) |
| stability | data property | may | cca:stability | Data stability (fixed/growing/revisable) |
| scale | data property | should | schema:spatialCoverage | Geographic extent of network action |
| variables | object property | may | schema:variableMeasured | Parameter names and units |
| acquisition method | data property | may | cca:acquisitionMethod | Collection/creation methods |
| acquisition frequency | data property | may | cca:acquisitionFrequency | Average acquisition frequency |
| survey automation | data property | may | cca:surveyAutomation | Automatic/manual collection |
| standard application | object property | may | dct:conformsTo | Standards/norms applied to data |
| sensitivity | object property | should | dpv:hasSensitivityLevel | Data sensitivity type |
| delay | data property | may | cca:dataRecoveryDelay | Average data recovery delays |
| volume | data property | may | dcat:byteSize | Average annual data volume |
| validation |data property |  may | cca:validationApproach | Data validation approach |
| qualification | data property | may | cca:qualityApproach | Data quality approach |
| format | data property | may | dct:format | Data format used |
| site number | data property | may | cca:stationsStudied | Number of stations studied |
| dataset number | data property | may | cca:datasetNumber | Number of datasets |

#### Processing

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Processing** | class | may | dpv:Processing | Defines the Processing contextual entity in the metadata model. Data processing beyond validation |
| has processing | object property | may | dpv:hasProcessing | Defines the relation to the Processing contextual entity in the metadata model |
| processing manager | object property | should | cca:processingManager | Processing/Analysis responsible |
| processing automation | data property | may | cca:processingAutomation | Automatic/manual processing |
| processing method | data property | may | cca:processingMethod | Processing methods/tools/protocols |
| processing delay | data property | may | schema:processingTime | Average processing time |
| pre-processing level | data property | may | cca:preProcessingLevel | Data levels before processing |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### Analyse

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Analysis** | class | may | dpv:Analyse | Defines the Analyse contextual entity in the metadata model. |
| has analysis | object property | may | dpv:hasProcessing | Defines the relationship with the Analyze contextual entity in the metadata model |
| analysis automation | data property | may | cca:analysisAutomation | Automatic/manual analysis |
| analysis method | data property | may | cca:analysisMethod | Analysis methods/tools/protocols |
| analysis delay | data property | may | schema:processingTime | Average analysis time |
| pre-analysis level | data property | may | cca:preAnalysisLevel | Data levels before analysis |
| post-analysis level | data property | may | cca:postAnalysisLevel | Data levels after analysis |
| products | data property | may | cca:hasProductNames | Product names |
| data reuse | data property | may | cca:reuseData | Reuse of existing data |

#### Store

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Store** | class | may | dpv:Store | Defines the Store contextual entity in the metadata model |
| has conservation | object property | should | dpv:hasProcessing | Defines relationship with the conservation (Store) contextual entity|
| conservation manager | object property | should | cca:conservationManager | Storage/Archiving responsible |
| storage archiving | data property | may | dct:type | Storage vs archiving distinction |
| procedure | data property | should | schema:procedure | Storage/archiving procedure |
| data selection | data property | should | cca:dataSelectionMethod | Data selection method |
| convention | data property | should | cca:fileNamingConvention | File naming convention |
| support | data property | should | cca:supportType | Storage/archiving support type |
| location | object property | should | schema:location | Storage/archiving location |
| conservation delay | data property | should | schema:duration | Storage/archiving duration |
| retrieval | object property | may | dpv:hasOrganisationalMeasure | Data recovery methods |
| securing | object property | may | dpv:hasTechnicalMeasure | Data access security methods |

#### Access

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Access** | class | may | dpv:Access | Defines the Access contextual entity in the metadata model |
| has access | object property | may | dpv:hasProcessing | Defines the relationship with the Access contextual entity |
| access manager | object property | should | cca:dataAccessManager | Data access responsible |
| dissemination principle | object property | should | dct:accessRights | Dissemination principle |
| mechanism | data property | should | schema:procedure | Access procedure to visualization tools |
| dissemination delay | data property | may | schema:processingTime | Average dissemination time |
| embargo period | data property | should | fabio:hasEmbargoDuration | Data embargo period |
| database | data property | may | cca:databaseAvailability | Database availability |
| carrier organisation | data property | may | cca:repositoryName<br>cca:organisationName | Repository and organization name |
| data model | objetct property | may | dct:conformsTo | Data schema/model used |
| management system | object property | may | dcat:accessService | Database management system |
| history | data property | may | adms:versionNotes | Version history visualization |

#### Disseminate

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Disseminate** | class | may | dpv:Disseminate | Defines the Disseminate contextual entity in the metadata model |
| has dissemination/reuse | may | dpv:hasProcessing | Defines the relationship with the Dissemitate contextual entity |
| dissemination manager | object property | should | cca:dataDissimiationManager | Dissemination/Reuse responsible |
| identifier | data property | may | schema:identifier | Data identifier (ARK, DOI, Handle, etc.) |
| integrity | data property | may | cca:integrityMethods | Data integrity methods |
| traceability | data property | may | cca:traceabilityMethods | Data traceability methods |
| license | object property | may | schema:license | License type (BY, ND, NC, SA) |
| publication | data property | should | cca:relatedPublications | Average number of associated publications |
| metadata | object property | should | foaf:isPrimaryTopicOf | Associated metadata |
| intelligibility | object property | may | schema:documentation | Documents for data intelligibility |

### Campaign Metadata Structure

#### Campaign

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Campaign** | class | may | cca:Campaign | Defines the Campaign contextual entity in the metadata model |
| has campaign | object property | may | cca:hasCampaign | Defines the relationship with the Campaign contextual entity  |
| identifier | data property | may | schema:identifier | Campaign with DOI |
| equipment | data property | may | cca:equipmentUsed | For example: glider, mooring, mastodon, CTD, coring |
| deployment date | data property | may | schema:temporalCoverage | Start and end dates |
| geographic coverage | object property | may | schema:spatialCoverage | Position of sampling/measurements |
| sensors | object property | may | sosa:madeBySensor | For example: salinity, temperature, turbidity, oxygen |
| measurement level | object property | may | sosa:usedProcedure | In water column, at surface, at bottom |
| acquisition frequency | data property | may | schema:frequency | Measurement frequency |
| parameters | object property | may | sosa:observedProperty | For example: conductivity |
| unit | data property | may | schema:unitCode | With possible justification for unit choice if subject to discussion |
| data type | data property | may | schema:contentType | For example: numerical (databases, spreadsheets), textual, image, audio, video |
| format / Access Software | data property | may | dct:format | File extension (pdf, xls, doc, txt, rdf) |
| volumes | data property | may | dcat:size | Storage space required, quantities of objects, files, rows, columns |
| metadata | object property | may | dct:conformsTo | Metadata standards used (DDI, TEI, EML, MARC, CMDI) |
| format | data property | may | cca:metadataFormat | Metadata format |
| quality control measures | data property | may | dcso:dataQualityAssurance | Precision, sensitivity, data quality measurement protocol |
| storage mode | data property | may | dpv:hasTechnicalOrganisationalMeasure | Repository, access and security (who has access, where, backup) |
| DOI | data property | may | bibo:doi | Associated datasets |
| equipment failure | data property | may | cca:equipmentFailure | Justifications (sensor failures, etc.) |

#### Model

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Model** | class | may | tech:Model | Defines the Model contextual entity in the metadata model |
| has model | object property | may | tech:hasModel | Defines the relationship with the Model contextual entity |
| model / neural network | data property | may | dct:type | Model type, neural network architecture |
| climate considered | data property | may | cca:climateConsidered | Current, future (period) |
| input data | object property | may | tech:hasInputData | Model input data |
| model failures | data property | may | cca:modelFailure | Justifications (simulation crashes, etc.) |

#### Satellite

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Satellite** | class | may | cca:Satellite | Defines the Satellite contextual entity in the metadata model |
| has satellite | object property | may | cca:hasSatellite | Defines the relationship with the Satellite contextual entity |
| campaign or satellite Mission | data property | may | cca:hasMission | Campaign with DOI, mission name (e.g., Sentinel) |

#### Document

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Document metadata** | class | may | foaf:Document | Defines the Document contextual entity in the metadata model |
| has document metadata | object property | may | foaf:isPrimaryTopicOf | Defines the relationship with the Document contextual entity |
| document type | data property | may | dct:type | Textual (recommendation documents, synthesis), image, audio, video |

### Auxiliary entities

#### Place

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Place** | class | may | schema:Place | Defines the Place contextual entity in the metadata model |
| geo | object property | may | schema:geo | Defines a relationship of Place and a GeoCoordinate or GeoShape |
| name | data property | may | schema:name | Captures the literal value for name (e.g., number, text, date). |
| address | data property | may | schema:address | Captures the literal value for address (e.g., number, text, date). |
| latitude | data property | may | schema:latitude | Captures the literal value for latitude (e.g., number, text, date). |
| longitude | data property | may | schema:longitude | Captures the literal value for longitude (e.g., number, text, date). |

#### GeoCoordinate

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **GeoCoordinate** | class | may | schema:GeoCoordinate | Defines the GeoCoordinate contextual entity in the metadata model |
| latitude | data property | may | schema:latitude | Captures the literal value for latitude (e.g., number, text, date) |
| longitude | data property | may | schema:longitude | Captures the literal value for longitude (e.g., number, text, date) |

#### GeoShape

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **GeoShape** | class | may | schema:GeoShape | Defines the GeoShape contextual entity in the metadata model |
| polygon | data property | may | schema:polygon | Captures the literal value for polygon (e.g., number, text, date) |
| box | data property | may | schema:box | Captures the literal value for box (e.g., number, text, date) |

#### Provenance Statement

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Provenance Statement** | class | may | dct:ProvenanceStatement | Defines the Provenance Statement contextual entity in the metadata model |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### Person

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Person** | class | may | schema:Person | Defines the Person contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |

#### Organisation

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Organisation** | class | may | schema:Organisation | Defines the Organisation contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |

#### Grant

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Grant** | class | may | schema:Grant | Defines the Grant contextual entity in the metadata model. |
| funder | object property | may | schema:funder | Defines a relationship for funder between metadata entities |
| name | data property | may | schema:name | Captures the literal value for name  |
| url | data property | may | schema:url | Captures the literal value for url |
| identifier | data property | may | schema:identifier | Captures the literal value for identifier (e.g., number, text, date) |

#### Standard

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Standard** | class | may | dct:Standard | Defines the Standard contextual entity in the metadata model. |
| name | data property | may | schema:name | Captures the literal value for name |

#### SensitivityLevel

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **SensitivityLevel** | class | may | dpv:SensitivityLevel | Defines the SensitivityLevel contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |

#### Dataset

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Dataset** | class | may | schema:Dataset | Defines the Dataset entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name  |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |
| identifier | data property | may | schema:identifier | Captures the literal value for identifier (e.g., number, text, date) |

#### DisasterRecoveryProcedures

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **DisasterRecoveryProcedures** | class | may | dpv:DisasterRecoveryProcedures | Defines the DisasterRecoveryProcedures contextual entity in the metadata model. |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### AccessControlMethod

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **AccessControlMethod** | class | may | dpv:AccessControlMethod | Defines the AccessControlMethod contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### RightsStatement

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **RightsStatement** | class | may | dct:RightsStatement | Defines the RightsStatement contextual entity in the metadata model |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### DataService

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **DataService** | class | may | dcat:DataService | Defines the DataService entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |
| endpointURL | data property | may | dcat:endpointURL | Captures the literal value for endpointURL |

#### Sensor

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Sensor** | class | may | sosa:Sensor | Defines the Sensor contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### Procedure

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Procedure** | class | may | sosa:Procedure | Defines the Procedure contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### TechnicalOrganisationalMeasure

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **TechnicalOrganisationalMeasure** | class | may | dpv:TechnicalOrganisationalMeasure | Defines the TechnicalOrganisationalMeasure contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date) |

#### Creative Work

| Term name | type | should/may | Semantic term | Description (Purpose/Comments) |
|---|---|---|---|---|
| **Creative Work** | class | may | schema:CreativeWork | Defines the Creative Work contextual entity in the metadata model |
| name | data property | may | schema:name | Captures the literal value for name |
| description | data property | may | schema:description | Captures the literal value for description (e.g., number, text, date). |
| identifier | data property | may | schema:identifier | Captures the literal value for identifier (e.g., number, text, date) |


## Example

Describe system components here.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/) License.
