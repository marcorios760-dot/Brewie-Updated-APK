# Retrofit
-keep interface com.squareup.retrofit2.** { *; }
-keepclasseswithmembers class * {
    @retrofit2.http.<methods> <methods>;
}

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-keep class okhttp3.** { *; }
-keep interface okhttp3.** { *; }

# GSON
-keep class com.google.gson.** { *; }
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# Hilt
-keep class * extends dagger.internal.Factory
-keep class * extends dagger.internal.Binding
-keep class * extends dagger.internal.ProvisionBinding
-keep @dagger.hilt.android.HiltAndroidApp class *

# Timber
-dontwarn timber.**

# Android lifecycle
-keep class androidx.lifecycle.** { *; }
-keepclassmembers class * {
    *** onCreate(...);
}

# Native methods
-keepclasseswithmembernames class * {
    native <methods>;
}
