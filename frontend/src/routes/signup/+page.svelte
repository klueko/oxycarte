<script lang="ts">
	let email = '';
	let pathology = '';
	let sensitivity_level = '';
	let age: number = 0;
	let weight: number = 0;
	let activity_level = '';

	let message = '';

	async function submitForm() {
        try {
            const response = await fetch('http://localhost:5000/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    pathology,
                    sensitivity_level,
                    age,
                    weight,
                    activity_level,
                    created_at: new Date().toISOString()
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create user');
            }

            const data = await response.json();
            message = data.message;
            // Clear form after successful submission
            email = '';
            pathology = '';
            sensitivity_level = '';
            age = 0;
            weight = 0;
            activity_level = '';
        } catch (error) {
            console.error('Signup error:', error);
            message = error instanceof Error ? error.message : 'An error occurred during signup';
        }
    }
</script>

<form on:submit|preventDefault={submitForm} class="space-y-4 p-4 max-w-md mx-auto">
	<input type="email" bind:value={email} placeholder="Email" required class="w-full border p-2" />
	<input type="text" bind:value={pathology} placeholder="Pathology" class="w-full border p-2" />
	<input type="text" bind:value={sensitivity_level} placeholder="Sensitivity level" class="w-full border p-2" />
	<input type="number" bind:value={age} placeholder="Age" class="w-full border p-2" />
	<input type="number" bind:value={weight} placeholder="Weight (kg)" class="w-full border p-2" />
	<input type="text" bind:value={activity_level} placeholder="Activity level" class="w-full border p-2" />
	<button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Envoyer</button>
</form>

{#if message}
	<p class="mt-4 text-center">{message}</p>
{/if}
