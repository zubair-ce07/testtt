export function parse(data: object) {
  return Object.keys(data).map(key => {
    const object = data[key];
    
    return {
      title: key,
      origin: {
        input: object['Origin Input'],
        selection: object['Origin Selection'],
      },
      destination: {
        input: object['Destination Input'],
        selection: object['Destination Selection'],
      },
      passengers: {
        youth: object['Passengers']['Youth'],
        adults: object['Passengers']['Adults'],
        seniors: object['Passengers']['Seniors'],
        lapInfant: object['Passengers']['Lap Infant'],
        seatInfant: object['Passengers']['Seat Infant'],
      },
      arrival: object['Arrival'],
      departure: object['Departure']
    }
  })
}
