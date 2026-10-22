import os
import re

BUNDLE = r'''
=== settings.gradle.kts ===
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "TamanaApp"
include(":app")

=== build.gradle.kts ===
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}

=== gradle.properties ===
org.gradle.jvmargs=-Xmx2048M -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official

=== app/build.gradle.kts ===
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.tamana.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.tamana.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-ktx:1.9.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
}

=== app/src/main/AndroidManifest.xml ===
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Tamana">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Tamana">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>

=== app/src/main/res/values/strings.xml ===
<resources>
    <string name="app_name">طمأنينة</string>
    <string name="subtitle">لقلب أرهقته الحياة</string>
    <string name="reflection_text">ألا بذكر الله تطمئن القلوب</string>
    <string name="tasbeeh_label">عداد التسبيح والذكر</string>
    <string name="btn_count">اضغط للذكر</string>
    <string name="btn_reset">إعادة الصفر</string>
</resources>

=== app/src/main/res/values/themes.xml ===
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.Tamana" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">@color/emerald_primary</item>
        <item name="colorOnPrimary">@color/white</item>
        <item name="colorPrimaryContainer">@color/emerald_container</item>
        <item name="colorOnPrimaryContainer">@color/emerald_on_container</item>
        <item name="android:windowBackground">@color/background_light</item>
    </style>

    <color name="emerald_primary">#1B4D3E</color>
    <color name="emerald_container">#C8E6C9</color>
    <color name="emerald_on_container">#0D2818</color>
    <color name="white">#FFFFFF</color>
    <color name="background_light">#F4F9F5</color>
    <color name="text_dark">#1E2923</color>
    <color name="text_muted">#556B5D</color>
</resources>

=== app/src/main/res/drawable/ic_launcher_foreground.xml ===
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
  <path
      android:fillColor="#FFFFFF"
      android:pathData="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.42 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.42 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z"/>
</vector>

=== app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml ===
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:color="#1B4D3E"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>

=== app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml ===
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:color="#1B4D3E"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>

=== app/src/main/res/layout/activity_main.xml ===
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F4F9F5"
    android:padding="24dp">

    <TextView
        android:id="@+id/tvTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="48dp"
        android:text="@string/app_name"
        android:textColor="#1B4D3E"
        android:textSize="32sp"
        android:textStyle="bold"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <TextView
        android:id="@+id/tvSubtitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/subtitle"
        android:textColor="#556B5D"
        android:textSize="16sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/tvTitle" />

    <androidx.cardview.widget.CardView
        android:id="@+id/cardReflection"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="32dp"
        app:cardBackgroundColor="#FFFFFF"
        app:cardCornerRadius="16dp"
        app:cardElevation="4dp"
        app:layout_constraintTop_toBottomOf="@id/tvSubtitle">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="20dp"
            android:gravity="center">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="آية اليوم أو خواطر"
                android:textColor="#556B5D"
                android:textSize="14sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/tvReflection"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="12dp"
                android:gravity="center"
                android:text="@string/reflection_text"
                android:textColor="#1E2923"
                android:textSize="20sp"
                android:textStyle="bold" />
        </LinearLayout>
    </androidx.cardview.widget.CardView>

    <androidx.cardview.widget.CardView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        app:cardBackgroundColor="#FFFFFF"
        app:cardCornerRadius="16dp"
        app:cardElevation="4dp"
        app:layout_constraintTop_toBottomOf="@id/cardReflection">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="24dp"
            android:gravity="center">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="@string/tasbeeh_label"
                android:textColor="#556B5D"
                android:textSize="16sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/tvCounter"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="16dp"
                android:text="0"
                android:textColor="#1B4D3E"
                android:textSize="48sp"
                android:textStyle="bold" />

            <Button
                android:id="@+id/btnCount"
                android:layout_width="match_parent"
                android:layout_height="56dp"
                android:layout_marginTop="20dp"
                android:text="@string/btn_count"
                android:textSize="16sp"
                app:backgroundTint="#1B4D3E"
                app:cornerRadius="12dp" />

            <Button
                android:id="@+id/btnReset"
                style="Widget.Material3.Button.TextButton"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:text="@string/btn_reset"
                android:textColor="#556B5D" />
        </LinearLayout>
    </androidx.cardview.widget.CardView>

</androidx.constraintlayout.widget.ConstraintLayout>

=== app/src/main/java/com/tamana/app/MainActivity.kt ===
package com.tamana.app

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tvCounter = findViewById<TextView>(R.id.tvCounter)
        val btnCount = findViewById<Button>(R.id.btnCount)
        val btnReset = findViewById<Button>(R.id.btnReset)
        val tvReflection = findViewById<TextView>(R.id.tvReflection)

        val reflections = arrayOf(
            "ألا بذكر الله تطمئن القلوب",
            "إن مع العسر يسرا",
            "لا تحزن إن الله معنا",
            "فاذكروني أذكركم واشكروا لي ولا تكفرون",
            "ومن يتوكل على الله فهو حسبه"
        )

        val randomReflection = reflections[(Math.random() * reflections.size).toInt()]
        tvReflection.text = randomReflection

        btnCount.setOnClickListener {
            count++
            tvCounter.text = count.toString()
        }

        btnReset.setOnClickListener {
            count = 0
            tvCounter.text = count.toString()
        }
    }
}
'''

def main():
    parts = re.split(r'^=== (.+?) ===\n', BUNDLE, flags=re.M)
    for i in range(1, len(parts), 2):
        path = parts[i].strip()
        content = parts[i+1].lstrip('\n')
        
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {path}")

if __name__ == '__main__':
    main()
