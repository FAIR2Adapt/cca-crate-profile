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

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **MVP** | may |  | Defines the **MVP** entity in the metadata model. |
| Variable | should | schema:variableMeasured | Variables used in the models to produce the output |
| Depth level | should | schema:depth | Depth level of the analysis |
| Time range | should | schema:temporalCoverage | Time range of the data icluded in the output |
| Spatial extend (DGGS id/bbox) | should | schema:spatialCoverage | Spatial extend of the data icluded in the output |
| Scenario/run id | should | cca:scenarioId | Scenario/run id of the model output |
| Grid resolution | should | geodcat:spatialResolutionAsText | Grid resolution of the model output |
| Licence | should | schema:license | License of the output |
| Version DOI | should | schema:identifier | DOI of the output |
| Provenance URL | should | dct:provenance | Provenance URL of the model output |

### Variable

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Variable** | may |  | Defines the **Variable** entity in the metadata model. |
| Name | may |  | Captures the literal value for **Name** (e.g., number, text, date). |
| URL | may |  | Captures the literal value for **URL** (e.g., number, text, date). |

### I-ADOPT variable

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Variable** | may | iadopt:Variable | Defines the **Variable** entity in the metadata model. |
| Name | may | schema:name | Captures the literal value for **Name** (e.g., number, text, date). |
| URL | may | schema:url | Captures the literal value for **URL** (e.g., number, text, date). |

### Project-Level Metadata Fields

#### Project

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Project** | may | schema:Project | Defines the **Project** entity in the metadata model. |
| Data Management Plan Reference | may | cca:dmp_id | Identifies data managers for each type of data |
| Expected Deliverables | may | cca:expectedDeliverable | Lists planned outputs with timeline codes |
| Reused Data | may | cca:reusedData | Identifies external data sources |
| General WP Program | may | cca:generalWPProgram | Overview of data collection activities |

### Network Metadata Structure

#### Network

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Network** | may | cca:Network | Defines the **Network** entity in the metadata model. |
| Network Manager | may | cca:networkManager | Defines a relationship for **Network Manager** between metadata entities. |
| Name | should | schema:name | Network/SNO name |
| Data Manager | may | citedcat:dataManager geodcat:custodian | Data responsible persons |
| Scientific Coordination | may | geodcat:principalInvestigator | Scientific coordination lead |
| Partners | may | schema:member | Partner organizations |
| Labelling | may | rdfs:label | Labeling year (first and last) |
| ILICO Integration Year | may | cca:IlicoIntegrationYear | ILICO integration year |
| Scientific Issues | may | cca:scientificIssues | Research questions and objectives |
| Grants | may | schema:funding or schema:funder (if grant is not needed/known) | Funding organizations |
| Network Costs | may | cca:averageNetworkCost | Average infrastructure costs |
| Data Costs | may | cca:averageDataCost | Average data costs |

#### Dataset

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Dataset** | may |  | Defines the **Dataset** entity in the metadata model. |
| Data Creation/Collection | may | schema:dataset | Defines a relationship for **Data Creation/Collection** between metadata entities. |
| Data Creation Manager | should | citedcat:dataCollector | Data creation/collection responsible |
| Type | may | dct:type | Type of data (collected/produced) |
| Origin | should | dct:source | Data source type (observations/experimental/simulations/derived) |
| Nature | should | cca:dataNature | Data nature (textual/numerical/audiovisual/modeled/discipline-specific) |
| Stability | may | cca:stability | Data stability (fixed/growing/revisable) |
| Scale | should | schema:spatialCoverage | Geographic extent of network action |
| Variables | may | schema:variableMeasured | Parameter names and units |
| Acquisition Method | may | cca:acquisitionMethod | Collection/creation methods |
| Acquisition Frequency | may | cca:acquisitionFrequency | Average acquisition frequency |
| Survey Automation | may | cca:surveyAutomation | Automatic/manual collection |
| Standard Application | may | dct:conformsTo | Standards/norms applied to data |
| Sensitivity | should | dpv:hasSensitivityLevel | Data sensitivity type |
| Delay | may | cca:dataRecoveryDelay | Average data recovery delays |
| Volume | may | dcat:byteSize | Average annual data volume |
| Validation | may | cca:validationApproach | Data validation approach |
| Qualification | may | cca:qualityApproach | Data quality approach |
| Format | may | dct:format | Data format used |
| Site Number | may | cca:stationsStudied | Number of stations studied |
| Dataset Number | may | cca:datasetNumber | Number of datasets |

#### Processing

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Processing** | may |  | Defines the **Processing** entity in the metadata model. |
| Processing Manager | should | cca:processingManager | Processing/Analysis responsible |
| Processing | may | dpv:hasProcessing | Data processing beyond validation |
| Processing Automation | may | cca:processingAutomation | Automatic/manual processing |
| Processing Method | may | cca:processingMethod | Processing methods/tools/protocols |
| Processing Delay | may | schema:processingTime | Average processing time |
| Pre-processing Level | may | cca:preProcessingLevel | Data levels before processing |

#### Analysis

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Analysis** | may |  | Defines the **Analysis** entity in the metadata model. |
| Analysis Automation | may | cca:analysisAutomation | Automatic/manual analysis |
| Analysis Method | may | cca:analysisMethod | Analysis methods/tools/protocols |
| Analysis Delay | may | schema:processingTime | Average analysis time |
| Pre-analysis Level | may | cca:preAnalysisLevel | Data levels before analysis |
| Post-analysis Level | may | cca:postAnalysisLevel | Data levels after analysis |
| Products | may | cca:hasProductNames | Product names |
| Data Reuse | may | cca:reuseData | Reuse of existing data |

#### Store

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Store** | may |  | Defines the **Store** entity in the metadata model. |
| Conservation Manager | should | cca:conservationManager | Storage/Archiving responsible |
| Storage Archiving | may | dct:type | Storage vs archiving distinction |
| Procedure | should | schema:procedure | Storage/archiving procedure |
| Data Selection | should | cca:dataSelectionMethod | Data selection method |
| Convention | should | cca:fileNamingConvention | File naming convention |
| Support | should | cca:supportType | Storage/archiving support type |
| Location | should | schema:location | Storage/archiving location |
| Conservation Delay | should | schema:duration | Storage/archiving duration |
| Retrieval | may | dpv:hasOrganisationalMeasure | Data recovery methods |
| Securing | may | dpv:hasTechnicalMeasure | Data access security methods |

#### Access

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Access** | may |  | Defines the **Access** entity in the metadata model. |
| Access Manager | should | cca:dataAccessManager | Data access responsible |
| Dissemination Principle | should | dct:accessRights | Dissemination principle |
| Mechanism | should | schema:procedure | Access procedure to visualization tools |
| Dissemination Delay | may | schema:processingTime | Average dissemination time |
| Embargo Period | should | fabio:hasEmbargoDuration | Data embargo period |
| Database | may | cca:databaseAvailability | Database availability |
| Carrier Organisation | may | cca:repositoryName<br>cca:organisationName | Repository and organization name |
| Data Model | may | dct:conformsTo | Data schema/model used |
| Management System | may | dcat:accessService | Database management system |
| History | may | adms:versionNotes | Version history visualization |

#### Disseminate

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Disseminate** | may |  | Defines the **Disseminate** entity in the metadata model. |
| Dissemination Manager | should | cca:dataDissimiationManager | Dissemination/Reuse responsible |
| Identifier | may | schema:identifier | Data identifier (ARK, DOI, Handle, etc.) |
| Integrity | may | cca:integrityMethods | Data integrity methods |
| Traceability | may | cca:traceabilityMethods | Data traceability methods |
| License | may | schema:license | License type (BY, ND, NC, SA) |
| Publication | should | cca:relatedPublications | Average number of associated publications |
| Metadata | should | foaf:isPrimaryTopicOf | Associated metadata |
| Intelligibility | may | schema:documentation | Documents for data intelligibility |

### Campaign Metadata Structure

#### Campaign

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Campaign** | may |  | Defines the **Campaign** entity in the metadata model. |
| Campaign | may | schema:identifier | Campaign with DOI |
| Equipment | may | cca:equipmentUsed | For example: glider, mooring, mastodon, CTD, coring |
| Deployment Date | may | schema:temporalCoverage | Start and end dates |
| Geographic Coverage | may | schema:spatialCoverage | Position of sampling/measurements |
| Sensors | may | sosa:madeBySensor | For example: salinity, temperature, turbidity, oxygen |
| Measurement Level | may | sosa:usedProcedure | In water column, at surface, at bottom |
| Acquisition Frequency | may | schema:frequency | Measurement frequency |
| Parameters | may | sosa:observedProperty | For example: conductivity |
| Unit | may | schema:unitCode | With possible justification for unit choice if subject to discussion |
| Data Type | may | schema:contentType | For example: numerical (databases, spreadsheets), textual, image, audio, video |
| Format / Access Software | may | dct:format | File extension (pdf, xls, doc, txt, rdf) |
| Volumes | may | dcat:size | Storage space required, quantities of objects, files, rows, columns |
| Metadata | may | dct:conformsTo | Metadata standards used (DDI, TEI, EML, MARC, CMDI) |
| Format | may | cca:metadataFormat | Metadata format |
| Quality Control Measures | may | dcso:dataQualityAssurance | Precision, sensitivity, data quality measurement protocol |
| Storage Mode | may | dpv:hasTechnicalOrganisationalMeasure | Repository, access and security (who has access, where, backup) |
| DOI | may | bibo:doi | Associated datasets |
| Equipment Failure | may | cca:equipmentFailure | Justifications (sensor failures, etc.) |

#### Model

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Model** | may |  | Defines the **Model** entity in the metadata model. |
| Model / Neural Network | may | dct:type | Model type, neural network architecture |
| Climate Considered | may | cca:climateConsidered | Current, future (period) |
| Input Data | may | tech:hasInputData | Model input data |
| Model Failures | may | cca:modelFailure | Justifications (simulation crashes, etc.) |

### Auxiliary entities

#### Satellite

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Satellite** | may |  | Defines the **Satellite** entity in the metadata model. |
| Campaign or Satellite Mission | may |  | Captures the literal value for **Campaign or Satellite Mission** (e.g., number, text, date). |

#### Document

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Document** | may |  | Defines the **Document** entity in the metadata model. |
| Document Type | may |  | Captures the literal value for **Document Type** (e.g., number, text, date). |

#### Place

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Place** | may | schema:Place | Defines the **Place** entity in the metadata model. |
| geo | may | schema:geo | Defines a relationship for **geo** between metadata entities. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| address | may | schema:address | Captures the literal value for **address** (e.g., number, text, date). |
| latitude | may | schema:latitude | Captures the literal value for **latitude** (e.g., number, text, date). |
| longitude | may | schema:longitude | Captures the literal value for **longitude** (e.g., number, text, date). |

#### GeoCoordinate

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **GeoCoordinate** | may | schema:GeoCoordinate | Defines the **GeoCoordinate** entity in the metadata model. |
| latitude | may | schema:latitude | Captures the literal value for **latitude** (e.g., number, text, date). |
| longitude | may | schema:longitude | Captures the literal value for **longitude** (e.g., number, text, date). |

#### GeoShape

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **GeoShape** | may | schema:GeoShape | Defines the **GeoShape** entity in the metadata model. |
| polygon | may | schema:polygon | Captures the literal value for **polygon** (e.g., number, text, date). |
| box | may | schema:box | Captures the literal value for **box** (e.g., number, text, date). |

#### Provenance Statement

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Provenance Statement** | may | dct:ProvenanceStatement | Defines the **Provenance Statement** entity in the metadata model. |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### Person

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Person** | may | schema:Person | Defines the **Person** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |

#### Organisation

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Organisation** | may | schema:Organisation | Defines the **Organisation** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |

#### Grant

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Grant** | may | schema:Grant | Defines the **Grant** entity in the metadata model. |
| funder | may | schema:funder | Defines a relationship for **funder** between metadata entities. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| url | may | schema:url | Captures the literal value for **url** (e.g., number, text, date). |
| identifier | may | schema:identifier | Captures the literal value for **identifier** (e.g., number, text, date). |

#### Standard

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Standard** | may | dct:Standard | Defines the **Standard** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |

#### SensitivityLevel

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **SensitivityLevel** | may | dpv:SensitivityLevel | Defines the **SensitivityLevel** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |

#### Dataset

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Dataset** | may | schema:Dataset | Defines the **Dataset** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |
| identifier | may | schema:identifier | Captures the literal value for **identifier** (e.g., number, text, date). |

#### Processing

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Processing** | may | dpv:Processing | Defines the **Processing** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### DisasterRecoveryProcedures

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **DisasterRecoveryProcedures** | may | dpv:DisasterRecoveryProcedures | Defines the **DisasterRecoveryProcedures** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### AccessControlMethod

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **AccessControlMethod** | may | dpv:AccessControlMethod | Defines the **AccessControlMethod** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### RightsStatement

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **RightsStatement** | may | dct:RightsStatement | Defines the **RightsStatement** entity in the metadata model. |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### DataService

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **DataService** | may | dcat:DataService | Defines the **DataService** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |
| endpointURL | may | dcat:endpointURL | Captures the literal value for **endpointURL** (e.g., number, text, date). |

#### Sensor

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Sensor** | may | sosa:Sensor | Defines the **Sensor** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### Procedure

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Procedure** | may | sosa:Procedure | Defines the **Procedure** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### TechnicalOrganisationalMeasure

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **TechnicalOrganisationalMeasure** | may | dpv:TechnicalOrganisationalMeasure | Defines the **TechnicalOrganisationalMeasure** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |

#### Creative Work

| Term name | Should/May | Semantic term (Final mappings) | Description (Purpose/Comments) |
|---|---|---|---|
| **Creative Work** | may | schema:CreativeWork | Defines the **Creative Work** entity in the metadata model. |
| name | may | schema:name | Captures the literal value for **name** (e.g., number, text, date). |
| description | may | schema:description | Captures the literal value for **description** (e.g., number, text, date). |
| identifier | may | schema:identifier | Captures the literal value for **identifier** (e.g., number, text, date). |


## Example

Describe system components here.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/) License.
