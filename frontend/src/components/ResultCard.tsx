import { Tag } from './Tag';
import { LiaWalkingSolid } from 'react-icons/lia';
import { FaSnowflake } from 'react-icons/fa';
import { FaBusAlt } from 'react-icons/fa';
import { IoMdBus } from 'react-icons/io';

export interface Properties {
  bus_number: number;
  route: string;
  route_class: string;
  route_type: string;
  route_1: string;
  route_1_class: string;
  route_1_type: string;
  route_2: string;
  route_2_class: string;
  route_2_type: string;
  route_3: string;
  route_3_class: string;
  route_3_type: string;
  coordinates: [number, number][][]; // Ajuste para las coordenadas
}

export interface RouteData {
  properties: Properties;
  coordinates: [number, number][][]; 
}

export interface ResultCardProps {
  properties: Properties;
  onRouteSelect: (coordinates: [number, number][][]) => void; // Ajuste para las coordenadas
  isSelected: boolean; // Nueva prop para indicar si la ruta está seleccionada
}

export const ResultCard = ({ properties, onRouteSelect, isSelected }: ResultCardProps) => {
  const {
    bus_number,
    route,
    route_class,
    route_type,
    route_1,
    route_1_class,
    route_1_type,
    route_2,
    route_2_class,
    route_2_type,
    route_3,
    route_3_class,
    route_3_type,
    coordinates, // Asegúrate de desestructurar las coordenadas
  } = properties;

  const handleSetRoute = (event: React.MouseEvent) => {
    event.stopPropagation(); // Detiene la propagación del evento
    console.log('Route set:', coordinates);
    onRouteSelect(coordinates); // Llama al manejador de selección de ruta
  };

  const renderTag = (text: string, icon: any, color: string, icon2?: any) => (
    <Tag Text={text} Icon={icon} Color={color} Icon2={icon2} /> // Renderiza una etiqueta con los íconos y el color correspondiente
  );

  const containerClass = isSelected ? 'bg-gray-300' : ''; // Cambiar fondo si está seleccionado

  switch (bus_number) {
    case 1:
      return (
        <div className={`flex flex-wrap justify-center items-center w-full p-4 border-t-2 border-gray-400 ${containerClass}`} onClick={handleSetRoute}>
          <div className="flex flex-wrap gap-4 w-4/5">
            <Tag Icon={LiaWalkingSolid} Color='bg-[#000000]' />
            {renderTag(route, route_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#D51E71] flex-grow', route_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
            <Tag Icon={LiaWalkingSolid} Color='bg-[#000000]' />
          </div>
        </div>
      );
    case 2:
      return (
        <div className={`flex justify-center items-center w-full py-4 px-1 border-t-2 border-gray-400 ${containerClass}`} onClick={handleSetRoute}>
          <div className="flex flex-wrap gap-1 w-full">
            {renderTag(route_1, route_1_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#D51E71] min-w-[35%] fit', route_1_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
            <Tag Icon={LiaWalkingSolid} Color='bg-[#000000] w-[15%]' />
            {renderTag(route_2, route_2_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#7209B7] min-w-[35%] flex-grow', route_2_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
          </div>
        </div>
      );
    case 3:
      return (
        <div className={`flex flex-wrap items-center w-full p-4 border-t-2 border-gray-400 hover:bg-gray-100 ${containerClass}`} onClick={handleSetRoute}>
          <div className="flex flex-wrap gap-4 w-full">
            {renderTag(route_1, route_1_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#D51E71] min-w-[35%] flex-grow', route_1_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
            <Tag Icon={LiaWalkingSolid} Color='bg-[#000000] w-[15%]' />
            {renderTag(route_2, route_2_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#7209B7] min-w-[35%] flex-grow', route_2_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
            <Tag Icon={LiaWalkingSolid} Color='bg-[#000000] w-[15%]' />
            {renderTag(route_3, route_3_type === 'POR AUTOBUS' ? FaBusAlt : IoMdBus, 'bg-[#4361EE] min-w-[35%] flex-grow', route_3_class === 'EXCLUSIVO' ? FaSnowflake : undefined)}
          </div>
        </div>
      );
    default:
      return (
        <p>No hay resultados</p>
      );
  }
};
