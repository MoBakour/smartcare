export {};

declare global {
    interface IUser {
        id: string;
        name: string;
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
            infected: boolean;
            size: number;
            treatment: string;
        };
        created_at: string;
        updated_at: string;
    }
}
