<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-2">
          Comparaison d'Images
        </h1>
        <p class="text-lg text-gray-600">
          Découvrons à quel point vos images se ressemblent
        </p>
      </div>

      <div class="grid md:grid-cols-2 gap-8 mb-8">
        <div class="bg-white rounded-lg shadow-lg overflow-hidden transform transition hover:scale-105 duration-300">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">
              Image 1 📸
            </h2>
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-blue-500 transition-colors duration-200"
              :class="{ 'border-blue-500 bg-blue-50': preview1 }"
            >
              <input
                type="file"
                @change="handleImage1Change"
                accept=".jpg, .jpeg, .png"
                class="hidden"
                ref="fileInput1"
              >
              <div
                @click="$refs.fileInput1.click()"
                class="cursor-pointer"
              >
                <div v-if="!preview1" class="text-center p-8">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <p class="mt-2 text-sm text-gray-600">Cliquez pour choisir une image ⬆️</p>
                </div>
                <div v-else class="relative h-64">
                  <img :src="preview1" class="w-full h-full object-contain">
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg overflow-hidden transform transition hover:scale-105 duration-300">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">
              Image 2 📸
            </h2>
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-blue-500 transition-colors duration-200"
              :class="{ 'border-blue-500 bg-blue-50': preview2 }"
            >
              <input
                type="file"
                @change="handleImage2Change"
                accept=".jpg, .jpeg, .png"
                class="hidden"
                ref="fileInput2"
              >
              <div
                @click="$refs.fileInput2.click()"
                class="cursor-pointer"
              >
                <div v-if="!preview2" class="text-center p-8">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <p class="mt-2 text-sm text-gray-600">Cliquez pour choisir une image ⬆️</p>
                </div>
                <div v-else class="relative h-64">
                  <img :src="preview2" class="w-full h-full object-contain">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center">
        <button
          @click="compareImages"
          class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          :disabled="!image1 || !image2 || loading"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? 'Analyse en cours... 🔄' : 'Comparer les images 🎯' }}
        </button>
      </div>

      <div v-if="similarity !== null"
           class="mt-8 transform transition-all duration-500"
           :class="{'scale-100 opacity-100': similarity !== null, 'scale-95 opacity-0': similarity === null}">
        <div class="bg-white rounded-lg shadow-lg p-6 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-blue-50 to-purple-50 opacity-50"></div>
          <div class="relative">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ similarityMessage }}
            </h3>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div
                  class="h-4 rounded-full transition-all duration-1000 ease-out bg-gradient-to-r from-blue-500 to-purple-500"
                  :style="{ width: `${displayedSimilarity}%` }"
                ></div>
              </div>
              <span class="ml-4 text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
            {{ displayedSimilarity }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      image1: null,
      image2: null,
      preview1: null,
      preview2: null,
      similarity: null,
      loading: false,
      error: null
    }
  },
  computed: {
    displayedSimilarity() {
      return Math.max(0, Number(this.similarity?.toFixed(2)) || 0)
    },
    similarityMessage() {
      if (this.similarity === null) return ''
      if (this.displayedSimilarity === 0) return 'Ces personnes sont complètement différentes'
      if (this.displayedSimilarity > 90) return 'Wow, ces personnes sont presque identiques !'
      if (this.displayedSimilarity > 80) return 'Ces personnes se ressemblent beaucoup'
      if (this.displayedSimilarity > 60) return 'Il y a pas mal de similarités'
      if (this.displayedSimilarity > 40) return 'Il y a quelques ressemblances'
      if (this.displayedSimilarity > 20) return 'Ces personnes sont assez différentes'
      return 'Ces images sont très différentes'
    }
  },
  methods: {
    handleImage1Change(event) {
      const file = event.target.files[0]
      this.image1 = file
      this.preview1 = URL.createObjectURL(file)
      this.similarity = null
    },
    handleImage2Change(event) {
      const file = event.target.files[0]
      this.image2 = file
      this.preview2 = URL.createObjectURL(file)
      this.similarity = null
    },
    async compareImages() {
      if (!this.image1 || !this.image2) return
      this.loading = true
      this.error = null

      const formData = new FormData()
      formData.append('image1', this.image1)
      formData.append('image2', this.image2)

      try {
        const response = await fetch('/api/compare', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        if (response.ok) {
          this.similarity = data.similarity
        } else {
          this.error = data.error || 'Une erreur est survenue'
        }
      } catch {
        this.error = 'Échec de la comparaison des images'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
