import { FaLocationDot, FaRegCircleDot } from 'react-icons/fa6';
import { Button } from './Button';
import { Input } from './Input';
import { ResultCard, Properties } from './ResultCard';
import { RefObject, useState, useEffect } from 'react';
import { PiBroomBold } from 'react-icons/pi';
import { PulseLoader } from 'react-spinners'; // Importar el spinner
import logo from '../assets/logo.png';

interface SidebarProps {
  setFocusedInput: (input: 'origin' | 'destination') => void; // Función para establecer el input enfocado
  originRef: RefObject<HTMLInputElement>; // Referencia del input de origen
  destinationRef: RefObject<HTMLInputElement>; // Referencia del input de destino
  onGetRoute: () => void; // Función para obtener la ruta
  data: Properties[]; // Datos de las propiedades de las rutas
  onRouteSelect: (coordinates: [number, number][][], index: number) => void; // Consistente con App.tsx
  loading: boolean; // Añadir estado de carga
  onClean: () => void; // Añadir función de limpieza
}

export const Sidebar = ({
  setFocusedInput,
  originRef,
  destinationRef,
  onGetRoute,
  data,
  onRouteSelect,
  loading,
  onClean,
}: SidebarProps) => {
  const [selectedRouteIndex, setSelectedRouteIndex] = useState<number | null>(null); // Estado para la ruta seleccionada

  useEffect(() => {
    console.log('Sidebar data:', data); // Log de los datos del sidebar
  }, [data]);

  const handleRouteSelect = (coordinates: [number, number][][], index: number) => {
    setSelectedRouteIndex(index); // Establecer el índice de la ruta seleccionada
    onRouteSelect(coordinates, index); // Llamar a la función de selección de ruta
  };

  return (
    <div className="w-2/6 h-screen p-1 flex flex-col  overflow-y-auto">
      <div className='px-3'>
        <h1 className="font-montserrat font-black text-2xl text-center mt-4">
          Ubícate con Avissa
        </h1>
        <img src={logo} className='h-[150px] m-auto'/> {/* Logo de la aplicación */}
        <h3 className="font-montserrat font-bold text-sm mt-5 mb-1 tracking-widest">
          ORIGEN
        </h3>
        <Input
          text={'Desde'}
          Icon={FaRegCircleDot}
          inputRef={originRef}
          onFocus={() => setFocusedInput('origin')} // Establecer el input enfocado en origen
        />
        <h3 className="font-montserrat font-bold text-sm mt-5 mb-1 tracking-widest">
          DESTINO
        </h3>
        <Input
          text={'Hasta'}
          Icon={FaLocationDot}
          inputRef={destinationRef}
          onFocus={() => setFocusedInput('destination')} // Establecer el input enfocado en destino
        />
        <div className="self-center justify-center mt-6 flex flex-row gap-2">
          <Button onClick={onGetRoute} text='Calcular Ruta' color="bg-[#4361EE]" />
          {data.length > 0 && (
            <Button onClick={onClean} text={<PiBroomBold />} color="bg-[#D51E43] text-xl font-bold" /> 
          )}
        </div>
        <h3 className="font-montserrat font-bold text-sm mt-5  tracking-widest">
          RESULTADOS
        </h3>
      </div>

      {loading && (
        <div className="self-center mt-4">
          <PulseLoader color="#4A90E2" loading={loading} size={10} /> {/* Spinner de carga */}
        </div>
      )}
      <div className="mt-3">
        {data.length > 0 ? (
          data.map((properties, index) => (
            <ResultCard
              key={index}
              properties={properties}
              onRouteSelect={(coordinates) => handleRouteSelect(coordinates, index)} // Manejar la selección de la ruta
              isSelected={index === selectedRouteIndex} // Pasar el estado seleccionado
            />
          ))
        ) : (
          <p>Aún no hay resultados</p> // Mensaje cuando no hay resultados
        )}
      </div>
    </div>
  );
};
