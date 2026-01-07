
# Transit GeoRouter

**Transit GeoRouter** is a full-stack web application for public transportation in **San Francisco**, built using **GTFS data**, **Node.js**, **React**, **TypeScript**, and **PostgreSQL**.

This project provides tools to explore transit routes and stops, view schedules, and perform **GTFS-based trip planning** using official **SFMTA** data. The routing algorithm used is **RAPTOR**, as proposed in the paper referenced below. RAPTOR is a round-based algorithm that efficiently computes routes without relying on a graph network.

---

## Route Algorithms

### RAPTOR Overview

RAPTOR is a **label-setting, round-based routing algorithm** specifically designed for public transportation systems. Unlike graph-based shortest path algorithms (for example, Dijkstra), RAPTOR operates directly on **routes and trips**, avoiding the need to construct or traverse large time-expanded graphs.

The algorithm was introduced by **Delling et al.** in *“Round-Based Public Transit Routing”* (ALENEX 2012) and is designed to answer earliest-arrival queries efficiently while scaling well to large metropolitan transit systems such as San Francisco.

**Delling, D., Pajor, T., & Werneck, R. F.**  
*Round-Based Public Transit Routing*  
Microsoft Research, ALENEX 2012  
https://www.microsoft.com/en-us/research/wp-content/uploads/2012/01/raptor_alenex.pdf

---

## Current goal

The existing RAPTOR solution relies on a **Python implementation**, based on the Transit Routing library(https://transnetlab.github.io/transit-routing/html/index.html)
The current goal of this project is to integrate **RAPTOR with a PostgreSQL-based GTFS schema**, enabling efficient data access and robust built-in POSTGIS support for spatial queries.

---

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Leaflet
- Fetch API / Axios

### Backend
- Python Flask

### Database
- PostgreSQL with **PostGIS** extension

### Data
- GTFS Static Feed (SFMTA)
---

## Inspiration
This repository is inspired by and **forked from https://github.com/Avissa-dev** 
