<script setup lang="ts">
import { ref } from "vue";
import { capitalize } from "../utils/utils";

interface Member {
    name: string;
    id: string;
    role: string;
    image?: string;
    link?: string;
}

interface Team {
    team: string;
    bg: string;
    members: Member[];
}

const data = ref<Team[]>([
    {
        team: "software",
        bg: "from-blue-400 to-purple-600",
        members: [
            {
                name: "Mohamed Bakour",
                id: "220911218",
                role: "Application Developer",
                image: "/members/bakour.jpg",
                link: "https://www.linkedin.com/in/mobakour/",
            },
            {
                name: "Hisham Elhamayel",
                id: "220911888",
                role: "Frontend Developer",
                image: "/members/hisham.png",
                link: "https://www.linkedin.com/in/hisham-elhamayel-b90746114/",
            },
            {
                name: "Amer Sinjab",
                id: "220911329",
                role: "UI/UX Designer",
                image: "/members/amer.png",
                link: "https://www.linkedin.com/in/amer-sinjab-8b9582310/",
            },
            {
                name: "Hussam Sarmini",
                id: "220911229",
                role: "Test and QA Specialist",
                image: "/members/hussam.png",
            },
            {
                name: "Mulham Sarmini",
                id: "220911223",
                role: "Test and QA Specialist",
                image: "/members/mulham.png",
            },
        ],
    },
    {
        team: "biomedical",
        bg: "from-green-400 to-lime-400",
        members: [
            {
                name: "Shahed Subhi",
                id: "220903320",
                role: "Biomedical Researcher",
            },
            {
                name: "Osama Alboushi",
                id: "220903240",
                role: "Biomedical Researcher",
            },
            {
                name: "Hassan Taha",
                id: "220903350",
                role: "Material Designer",
                image: "/members/hassan.png",
            },
            {
                name: "Mohamad Alhatab",
                id: "229910839",
                role: "Biomedical Engineer",
                link: "https://www.linkedin.com/in/mohammad-al-hatab-656738345/",
                image: "/members/hatab.png",
            },
        ],
    },
    {
        team: "computer",
        bg: "from-red-400 to-pink-600",
        members: [
            {
                name: "Osman Sirac",
                id: "190722054",
                role: "Work Assistant",
            },
            {
                name: "Bugrahan Yilmaz",
                id: "190722114",
                role: "Work Assistant",
            },
        ],
    },
]);
</script>

<template>
    <div class="mb-10">
        <h1 class="text-2xl">Say Hello to The Team</h1>

        <!-- team list -->
        <div>
            <div v-for="team in data" class="mt-10">
                <h2
                    class="text-xl font-bold bg-gradient-to-r bg-clip-text text-transparent w-fit"
                    :class="team.bg"
                >
                    {{ capitalize(team.team) }} Engineering Team
                </h2>

                <div
                    class="grid grid-cols-2 gap-x-5 gap-y-10 mt-6 max-[840px]:grid-cols-1"
                >
                    <a
                        v-for="member in team.members"
                        :href="member.link"
                        target="_blank"
                        class="flex gap-6 transition p-4 rounded-xl"
                        :class="member.link ? 'hover:bg-gray-100' : ''"
                    >
                        <div
                            class="w-[140px] min-w-[140px] h-[140px] bg-gray-300 rounded-xl overflow-hidden flex items-center justify-center"
                        >
                            <img
                                v-if="member.image"
                                :src="member.image"
                                class="w-full h-full object-cover"
                            />
                            <i-solar-user-outline v-else class="text-5xl" />
                        </div>

                        <div
                            class="whitespace-nowrap flex flex-col justify-center"
                        >
                            <p class="font-bold text-lg">{{ member.name }}</p>
                            <p class="text-sm text-gray-400">{{ member.id }}</p>
                            <p
                                class="text-sm bg-gradient-to-r bg-clip-text text-transparent w-fit"
                                :class="team.bg"
                            >
                                {{ member.role }}
                            </p>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>
