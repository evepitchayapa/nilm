export class Data
{
    _id: number;
    type: Date;
    active: number;
    current:number;
    voltage: number;
    frequency: number;
    reactive: number;
    apparent: number;
    date: Date;
    appliance: string;
    hour: number;

    constructor (_id,type,active,current,voltage,frequency,reactive,apparent,date,appliance,hour){
        this._id =_id;
        this.type = type;
        this.active = active;
        this.current = current;
        this.voltage = voltage;
        this.frequency = frequency;
        this.reactive = reactive;
        this.apparent = apparent;
        this.date = date;
        this.appliance = appliance;
        this.hour = hour;
    }
}