export {};

declare global {
    interface IUser {
        id: string;
        username: string;
        email: string;
        role: string;
    }

    interface IPatient {
        _id: string;
        supervisor: string;
        name: string;
        avatar: string;
        gender: string;
        age: number;
        bed: number;
        department: string;
        blood_type: string;
        wound: {
            type: string;
            location: string;
            severity: string;
            infected: string;
            size: number;
            treatment: string;
        };
        created_at: string;
        updated_at: string;
    }

    interface PatientHealthIndicators {
        Time: number;
        "Wound Temperature": number;
        "Wound pH": number;
        "Moisture Level": number;
        "Drug Release": number;
        "Healing Time": number;
    }
}
