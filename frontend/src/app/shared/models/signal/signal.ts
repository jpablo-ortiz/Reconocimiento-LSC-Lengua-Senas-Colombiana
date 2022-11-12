export class Signal {

    public name: string;
    public images: string[];
    public processed_signal: boolean;

    constructor(name?: string, images?: string[], processed_signal?: boolean) {
        this.name = name || '';
        this.images = images || [];
        this.processed_signal = processed_signal || false;
    }
}
