<script lang="ts">
    import { goto } from '$app/navigation';
    let email = '';
    let pathology = '';
    let age: number = 0;
    let weight: number = 0;
    let familyMembers: { name: string; pathology: string, age?: number }[] = [];
    let message = '';
    let otherPathology = '';

    const pathologyOptions = [
        { value: '', label: 'Sélectionnez une pathologie' },
        { value: 'asthme', label: 'Asthme' },
        { value: 'bpco', label: 'BPCO (Bronchopneumopathie Chronique Obstructive)' },
        { value: 'bronchite', label: 'Bronchite chronique' },
        { value: 'autre', label: 'Autre' }
    ];
    
    function addFamilyMember() {
        familyMembers.push({ name: '', pathology: '', age: undefined });
        familyMembers = [...familyMembers];
    }
    function removeFamilyMember(index: number) {
        familyMembers.splice(index, 1);
        familyMembers = [...familyMembers];
    }
    async function submitForm() {
        try {
            const response = await fetch('http://localhost:5000/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    pathology: pathology === 'autre' ? otherPathology : pathology,
                    age,
                    family: familyMembers,
                    created_at: new Date().toISOString()
                })
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'impossible de créer l\'utilisateur');
            }
            const data = await response.json();
            message = data.message;
            email = '';
            pathology = '';
            age = 0;
            familyMembers = [];
            goto('/');
        } catch (error) {
            console.error('Signup error:', error);
            message = error instanceof Error ? error.message : 'Une erreur est survenue';
        }
    }
</script>

<div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full mx-auto">
        <div class="text-center mb-6">
            <h2 class="text-3xl font-extrabold text-gray-900">Créer un compte</h2>
            <p class="mt-2 text-sm text-gray-600">Veuillez remplir le formulaire ci-dessous</p>
        </div>

        <form on:submit|preventDefault={submitForm} class="bg-white py-8 px-6 shadow rounded-lg space-y-6">
            <!-- Email Field -->
            <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Adresse email</label>
                <input 
                    type="email" 
                    id="email"
                    bind:value={email} 
                    placeholder="votreemail@exemple.com" 
                    required 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                />
            </div>
            
            <div>
                <label for="pathology" class="block text-sm font-medium text-gray-700 mb-1">Pathologie respiratoire</label>
                <select 
                    id="pathology"
                    bind:value={pathology} 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                    {#each pathologyOptions as option}
                        <option value={option.value}>{option.label}</option>
                    {/each}
                </select>

                {#if pathology === 'bpco'}
                <div class="mt-1 text-xs text-gray-500 bg-blue-50 p-2 rounded-md">
                    <span class="font-medium">BPCO :</span> Maladie respiratoire chronique caractérisée par une obstruction progressive des voies aériennes, souvent liée au tabagisme.
                </div>
                {/if}

                {#if pathology === 'autre'}
                <div class="mt-2">
                    <input 
                        type="text" 
                        bind:value={otherPathology} 
                        placeholder="Précisez votre pathologie" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                    />
                </div>
                {/if}
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label for="age" class="block text-sm font-medium text-gray-700 mb-1">Âge</label>
                    <input 
                        type="number" 
                        id="age"
                        bind:value={age} 
                        min="0"
                        placeholder="Âge" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                    />
                </div>
            </div>
            
            <!-- Family Members Section -->
            <div class="border-t border-gray-200 pt-5">
                <h3 class="text-lg font-medium text-gray-900 mb-3">Famille & particularités de santé</h3>
                
                {#if familyMembers.length === 0}
                    <p class="text-sm text-gray-500 italic mb-2">Aucun membre de famille ajouté</p>
                {/if}
                
                {#each familyMembers as member, index}
                    <div class="bg-gray-50 p-3 rounded-md mb-3">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm font-medium text-gray-700">Membre #{index + 1}</span>
                            <button 
                                type="button" 
                                on:click={() => removeFamilyMember(index)}
                                class="text-red-500 hover:text-red-700 focus:outline-none"
                                aria-label="Supprimer ce membre de la famille"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>
                        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                            <div>
                                <input 
                                    type="text" 
                                    bind:value={member.name} 
                                    placeholder="Nom" 
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                                />
                            </div>
                            <div>
                                <input 
                                    type="number" 
                                    bind:value={member.age} 
                                    placeholder="Âge" 
                                    min="0"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                                />
                            </div>
                            <div>
                                <!-- <input 
                                    type="text" 
                                    bind:value={member.pathology} 
                                    placeholder="Condition de santé" 
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                                /> -->
                                <label for="pathology" class="block text-sm font-medium text-gray-700 mb-1">Pathologie respiratoire</label>
                                <select 
                                    id="pathology"
                                    bind:value={pathology} 
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                >
                                    {#each pathologyOptions as option}
                                        <option value={option.value}>{option.label}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>
                            {#if member.age !== undefined && member.age < 15}
                            <div class="mt-1 text-xs text-gray-500 bg-blue-50 p-2 rounded-md">
                                <span class="font-medium"><p class="font-medium mb-1">Les <strong>enfants</strong> sont particulièrement sensibles à plusieurs polluants atmosphériques car :</p>
                                <ul class="list-disc pl-5 space-y-1">
                                    <li>Leurs <strong>voies respiratoires sont encore en développement</strong>.</li>
                                    <li>Ils respirent <strong>plus d'air par kilo de poids</strong> que les adultes.</li>
                                    <li>Ils sont plus souvent à l'extérieur (donc plus exposés).</li>
                                </ul>
                            </div>
                            {/if}
                {/each}
                
                <button 
                    type="button" 
                    on:click={addFamilyMember} 
                    class="mt-2 flex items-center text-sm font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
                    </svg>
                    Ajouter un membre de famille
                </button>
            </div>
            
            <!-- Submit Button -->
            <div>
                <button 
                    type="submit" 
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150"
                >
                    Créer mon compte
                </button>
            </div>
        </form>
        
        {#if message}
            <div class="mt-4 p-3 {message.includes('erreur') ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'} rounded-md text-center">
                {message}
            </div>
        {/if}
    </div>
</div>