import { useEffect } from 'react';
import { MapContainer, Marker, TileLayer, GeoJSON, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Feature, Geometry } from 'geojson';
import charmander from '../assets/charmander.png';
import { LocateButton } from './LocateButton';

interface MapProps {
  setOrigin: (location: [number, number]) => void; // Función para establecer el origen
  setDestination: (location: [number, number]) => void; // Función para establecer el destino
  origin: [number, number] | null; // Coordenadas del origen
  destination: [number, number] | null; // Coordenadas del destino
  onMapDoubleClick: (location: [number, number]) => void; // Función para manejar el doble clic en el mapa
  selectedRoutes: Feature<Geometry>[]; // Rutas seleccionadas a mostrar en el mapa
}

export const Map = ({ setOrigin, origin, destination, onMapDoubleClick, selectedRoutes }: MapProps) => {
  const position: [number, number] = [13.7036, -89.224]; // Coordenadas iniciales del centro del mapa

  useEffect(() => {
    console.log('Map received selectedRoute:', selectedRoutes); // Log para ver las rutas seleccionadas recibidas
  }, [selectedRoutes]);

  const defaultIcon = new L.Icon({
    iconUrl: charmander, // URL del icono del marcador
    iconSize: [40, 41], // Tamaño del icono
    iconAnchor: [12, 41], // Punto del icono que se ancla al mapa
    popupAnchor: [1, -34], // Punto desde donde se abrirá el popup
    shadowUrl: 'https://unpkg.com/leaflet@1.6/dist/images/marker-shadow.png', // URL de la sombra del icono
    shadowSize: [41, 41] // Tamaño de la sombra
  });

  const MapDoubleClickHandler = () => {
    useMapEvents({
      dblclick: e => {
        const { lat, lng } = e.latlng;
        onMapDoubleClick([lat, lng]); // Llamar a la función cuando se hace doble clic en el mapa
      }
    });
    return null;
  };

  return (
    <MapContainer center={position} zoom={13} className="h-screen w-full"> {/* Contenedor del mapa */}
      <TileLayer
        url="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}" // URL del tile layer de Google Maps
        maxZoom={20} // Zoom máximo permitido
        subdomains={['mt0', 'mt1', 'mt2', 'mt3']} // Subdominios utilizados
      />
      <MapDoubleClickHandler /> {/* Manejador del doble clic */}
      <LocateButton setOrigin={setOrigin} /> {/* Botón de localización */}
      {origin && <Marker position={origin} icon={defaultIcon} />} {/* Marcador para el origen */}
      {destination && <Marker position={destination} icon={defaultIcon} />} {/* Marcador para el destino */}
      {selectedRoutes.map((route, index) => (
        <GeoJSON
          key={index}
          data={route} // Datos de la ruta en formato GeoJSON
          style={() => ({
            color: route.properties?.color || '#000000', // Color de la ruta
            weight: 5, // Grosor de la línea de la ruta
            opacity: 0.8, // Opacidad de la línea de la ruta
          })}
        />
      ))}
    </MapContainer>
  );
};
