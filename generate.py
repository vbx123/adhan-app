import os
import re
import shutil

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
rootProject.name = "NightAdhan"
include(":app")
=== build.gradle.kts ===
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
=== gradle.properties ===
org.gradle.jvmargs=-Xmx3g -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
=== app/build.gradle.kts ===
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.nightadhan.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.nightadhan.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 2
        versionName = "2.0"
    }

    androidResources {
        noCompress.addAll(listOf("mp3", "ogg", "m4a", "wav", "aac", "opus"))
    }

    buildTypes {
        release {
            isMinifyEnabled = false
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
}
=== app/src/main/AndroidManifest.xml ===
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />
    <uses-permission android:name="android.permission.USE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" android:maxSdkVersion="32" />

    <queries>
        <intent>
            <action android:name="android.intent.action.TTS_SERVICE" />
        </intent>
    </queries>

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:label="مؤذن"
        android:supportsRtl="true"
        android:theme="@style/Theme.Night">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".AdhanService"
            android:exported="false"
            android:foregroundServiceType="mediaPlayback" />

        <service
            android:name=".DhikrService"
            android:exported="false"
            android:foregroundServiceType="mediaPlayback" />

        <receiver
            android:name=".AlarmReceiver"
            android:exported="false" />

        <receiver
            android:name=".DhikrReceiver"
            android:exported="false" />

        <receiver
            android:name=".BootReceiver"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.TIMEZONE_CHANGED" />
                <action android:name="android.intent.action.TIME_SET" />
            </intent-filter>
        </receiver>
    </application>
</manifest>
=== app/src/main/res/values/themes.xml ===
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Night" parent="@android:style/Theme.Material.NoActionBar">
        <item name="android:windowBackground">@android:color/black</item>
        <item name="android:statusBarColor">#0A0E1A</item>
        <item name="android:navigationBarColor">#131A2E</item>
        <item name="android:colorAccent">#F2C46D</item>
        <item name="android:colorPrimary">#131A2E</item>
    </style>
</resources>
=== app/src/main/res/drawable/ic_launcher.xml ===
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#0A0E1A"
        android:pathData="M0,0h24v24h-24z" />
    <path
        android:fillColor="#F2C46D"
        android:pathData="M12,3c-4.97,0 -9,4.03 -9,9s4.03,9 9,9 9,-4.03 9,-9c0,-0.46 -0.04,-0.92 -0.1,-1.36 -0.98,1.37 -2.58,2.26 -4.4,2.26 -2.98,0 -5.4,-2.42 -5.4,-5.4 0,-1.81 0.89,-3.42 2.26,-4.4C12.92,3.04 12.46,3 12,3z" />
</vector>
=== app/src/main/res/drawable/ic_stat.xml ===
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFFFF"
        android:pathData="M12,3c-4.97,0 -9,4.03 -9,9s4.03,9 9,9 9,-4.03 9,-9c0,-0.46 -0.04,-0.92 -0.1,-1.36 -0.98,1.37 -2.58,2.26 -4.4,2.26 -2.98,0 -5.4,-2.42 -5.4,-5.4 0,-1.81 0.89,-3.42 2.26,-4.4C12.92,3.04 12.46,3 12,3z" />
</vector>
=== app/src/main/java/com/nightadhan/app/Util.kt ===
package com.nightadhan.app

import android.content.Context
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.widget.TextView
import android.widget.Toast
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import java.util.Calendar
import java.util.Locale

object Night {
    var BG = 0
    var CARD = 0
    var CARD2 = 0
    var GOLD = 0
    var TEAL = 0
    var TEXT = 0
    var MUTED = 0
    var light = false

    val HERO1 = Color.parseColor("#2A3F73")
    val HERO2 = Color.parseColor("#131A2E")
    val HEROTEXT = Color.parseColor("#EAEDF7")
    val HEROGOLD = Color.parseColor("#F2C46D")
    val HEROMUTED = Color.parseColor("#B6BEDB")
    val SPLASH_BG = Color.parseColor("#0A0E1A")
    val SPLASH_BG2 = Color.parseColor("#14203F")

    val onGold: Int
        get() = if (light) Color.WHITE else Color.parseColor("#0A0E1A")

    init {
        apply(0)
    }

    fun apply(theme: Int) {
        light = theme == 2
        when (theme) {
            1 -> {
                BG = Color.parseColor("#000000")
                CARD = Color.parseColor("#0F1118")
                CARD2 = Color.parseColor("#1B1E2A")
                GOLD = Color.parseColor("#F2C46D")
                TEAL = Color.parseColor("#4DD0B5")
                TEXT = Color.parseColor("#EAEDF7")
                MUTED = Color.parseColor("#8B93B0")
            }
            2 -> {
                BG = Color.parseColor("#F3F4F9")
                CARD = Color.parseColor("#FFFFFF")
                CARD2 = Color.parseColor("#E7EAF4")
                GOLD = Color.parseColor("#A47A12")
                TEAL = Color.parseColor("#00897B")
                TEXT = Color.parseColor("#151A2E")
                MUTED = Color.parseColor("#5C6482")
            }
            else -> {
                BG = Color.parseColor("#0A0E1A")
                CARD = Color.parseColor("#131A2E")
                CARD2 = Color.parseColor("#1D2742")
                GOLD = Color.parseColor("#F2C46D")
                TEAL = Color.parseColor("#4DD0B5")
                TEXT = Color.parseColor("#EAEDF7")
                MUTED = Color.parseColor("#8B93B0")
            }
        }
    }
}

object Icons {
    private var tf: Typeface? = null
    private var loaded = false

    fun face(ctx: Context): Typeface? {
        if (!loaded) {
            loaded = true
            tf = try {
                Typeface.createFromAsset(ctx.applicationContext.assets, "icons.otf")
            } catch (e: Exception) {
                null
            }
        }
        return tf
    }
}

fun Context.prefs(): SharedPreferences =
    getSharedPreferences("adhan", Context.MODE_PRIVATE)

fun Context.toast(m: String) {
    Toast.makeText(this, m, Toast.LENGTH_LONG).show()
}

fun Context.dp(v: Int): Int =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()

fun Context.roundBg(color: Int, radiusDp: Int): GradientDrawable =
    GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(radiusDp).toFloat()
    }

fun Context.tv(text: String, size: Float, color: Int, bold: Boolean = false): TextView =
    TextView(this).apply {
        this.text = text
        textSize = size
        setTextColor(color)
        if (bold) setTypeface(typeface, Typeface.BOLD)
    }

fun Context.iconView(name: String, sizeSp: Float, color: Int): TextView =
    TextView(this).apply {
        val f = Icons.face(this@iconView)
        if (f != null) {
            typeface = f
            text = name
            fontFeatureSettings = "'liga'"
        } else {
            text = ""
        }
        textSize = sizeSp
        setTextColor(color)
        includeFontPadding = false
        gravity = Gravity.CENTER
        isAllCaps = false
    }

fun TextView.setIcon(name: String) {
    text = if (Icons.face(context) != null) name else ""
}

fun alpha(c: Int, a: Int): Int = (c and 0x00FFFFFF) or (a shl 24)

fun arNum(ctx: Context, s: String): String {
    val arabic = ctx.prefs().getBoolean("ar_digits", true)
    val sb = StringBuilder()
    for (ch in s) {
        val d = when (ch) {
            in '0'..'9' -> ch - '0'
            in '٠'..'٩' -> ch - '٠'
            else -> -1
        }
        if (d < 0) sb.append(ch)
        else if (arabic) sb.append('٠' + d)
        else sb.append('0' + d)
    }
    return sb.toString()
}

fun clockText(ctx: Context, ms: Long): String {
    val c = Calendar.getInstance()
    c.timeInMillis = ms
    if (ctx.prefs().getBoolean("h24", false)) {
        return arNum(
            ctx,
            String.format(Locale.US, "%02d:%02d", c.get(Calendar.HOUR_OF_DAY), c.get(Calendar.MINUTE))
        )
    }
    val h = c.get(Calendar.HOUR)
    val h12 = if (h == 0) 12 else h
    val m = c.get(Calendar.MINUTE)
    val suffix = if (c.get(Calendar.AM_PM) == Calendar.AM) "ص" else "م"
    return arNum(ctx, String.format(Locale.US, "%d:%02d", h12, m)) + " " + suffix
}

fun countdownText(ctx: Context, ms: Long): String {
    val total = if (ms < 0) 0L else ms / 1000
    val h = total / 3600
    val m = (total % 3600) / 60
    val s = total % 60
    return arNum(ctx, String.format(Locale.US, "%02d:%02d:%02d", h, m, s))
}
=== app/src/main/java/com/nightadhan/app/Sounds.kt ===
package com.nightadhan.app

import android.content.Context
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.net.Uri
import android.provider.OpenableColumns
import java.io.File

class SoundItem(val id: String, val label: String, val category: String, val name: String)

object Sounds {
    private val EXT = setOf("mp3", "ogg", "m4a", "wav", "aac", "opus")
    private var cache: List<SoundItem>? = null

    private fun categoryOf(name: String): String = when {
        name.startsWith("fajr_") -> "fajr"
        name.startsWith("adhan_") -> "adhan"
        name.startsWith("pre_") -> "pre"
        name.startsWith("dhikr_") -> "dhikr"
        name.startsWith("tone_") -> "tone"
        else -> "other"
    }

    private fun readLabels(ctx: Context): Map<String, String> {
        val m = HashMap<String, String>()
        try {
            ctx.assets.open("sounds/labels.txt").bufferedReader(Charsets.UTF_8).useLines { lines ->
                for (raw in lines) {
                    val line = raw.trim().trimStart('\uFEFF')
                    if (line.isEmpty() || line.startsWith("#")) continue
                    val i = line.indexOf('=')
                    if (i <= 0) continue
                    val k = line.substring(0, i).trim().substringBeforeLast('.')
                    val v = line.substring(i + 1).trim()
                    if (v.isNotEmpty()) m[k] = v
                }
            }
        } catch (e: Exception) {
            // no labels file
        }
        return m
    }

    fun builtin(ctx: Context): List<SoundItem> {
        val c = cache
        if (c != null) return c
        val labels = readLabels(ctx)
        val out = ArrayList<SoundItem>()
        try {
            val files = ctx.assets.list("sounds") ?: arrayOf()
            for (f in files.sorted()) {
                val ext = f.substringAfterLast('.', "").lowercase()
                if (ext !in EXT) continue
                val name = f.substringBeforeLast('.')
                out.add(SoundItem("builtin:" + f, labels[name] ?: name, categoryOf(name), name))
            }
        } catch (e: Exception) {
            // ignore
        }
        cache = out
        return out
    }

    fun customList(ctx: Context): List<SoundItem> {
        val raw = ctx.prefs().getString("custom_sounds", "") ?: ""
        val out = ArrayList<SoundItem>()
        for (line in raw.split("\n")) {
            val i = line.indexOf('|')
            if (i <= 0) continue
            val path = line.substring(0, i)
            if (File(path).exists()) {
                out.add(SoundItem("file:" + path, line.substring(i + 1), "custom", path))
            }
        }
        return out
    }

    fun addCustomBlocking(ctx: Context, uri: Uri): Boolean {
        return try {
            val dir = File(ctx.filesDir, "custom")
            dir.mkdirs()
            var name = "صوت مخصص"
            try {
                ctx.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use {
                    if (it.moveToFirst()) name = it.getString(0) ?: name
                }
            } catch (e: Exception) {
                // ignore
            }
            name = name.substringBeforeLast('.').replace("|", " ").replace("\n", " ")
            val f = File(dir, "s" + System.currentTimeMillis() + ".bin")
            val input = ctx.contentResolver.openInputStream(uri) ?: return false
            input.use { i -> f.outputStream().use { o -> i.copyTo(o) } }
            val p = ctx.prefs()
            val old = p.getString("custom_sounds", "") ?: ""
            val entry = f.absolutePath + "|" + name
            p.edit().putString("custom_sounds", if (old.isEmpty()) entry else old + "\n" + entry).apply()
            true
        } catch (e: Exception) {
            false
        }
    }

    fun labelOf(ctx: Context, id: String): String = when {
        id == "default" -> "نغمة النظام"
        id == "tts" -> "صوت ناطق (قراءة الذكر)"
        id == "none" -> "بدون صوت"
        id == "random" -> "عشوائي من الأصوات المتاحة"
        id.startsWith("builtin:") ->
            builtin(ctx).firstOrNull { it.id == id }?.label ?: id.removePrefix("builtin:")
        id.startsWith("file:") ->
            customList(ctx).firstOrNull { it.id == id }?.label ?: "ملف مخصص"
        else -> id
    }

    fun exists(ctx: Context, id: String): Boolean = when {
        id.startsWith("builtin:") -> builtin(ctx).any { it.id == id }
        id.startsWith("file:") -> File(id.removePrefix("file:")).exists()
        else -> true
    }

    fun defaultAdhan(ctx: Context, prayer: Int): String {
        val all = builtin(ctx)
        val pick = (if (prayer == 0) all.firstOrNull { it.category == "fajr" } else null)
            ?: all.firstOrNull { it.category == "adhan" }
        return pick?.id ?: "default"
    }

    fun defaultPre(ctx: Context): String {
        val all = builtin(ctx)
        val pick = all.firstOrNull { it.category == "pre" } ?: all.firstOrNull { it.category == "tone" }
        return pick?.id ?: "default"
    }

    fun randomFor(ctx: Context, prefix: String): String? {
        val l = builtin(ctx).filter { it.name.startsWith(prefix) }
        return if (l.isEmpty()) null else l.random().id
    }

    fun createPlayer(ctx: Context, id: String, usage: Int, content: Int): MediaPlayer? {
        val mp = MediaPlayer()
        return try {
            mp.setAudioAttributes(
                AudioAttributes.Builder().setUsage(usage).setContentType(content).build()
            )
            when {
                id.startsWith("builtin:") -> {
                    val afd = ctx.assets.openFd("sounds/" + id.removePrefix("builtin:"))
                    mp.setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                    afd.close()
                }
                id.startsWith("file:") -> mp.setDataSource(id.removePrefix("file:"))
                else -> {
                    val type = if (usage == AudioAttributes.USAGE_ALARM)
                        RingtoneManager.TYPE_ALARM else RingtoneManager.TYPE_NOTIFICATION
                    mp.setDataSource(ctx, RingtoneManager.getDefaultUri(type))
                }
            }
            mp
        } catch (e: Exception) {
            try {
                mp.release()
            } catch (e2: Exception) {
                // ignore
            }
            null
        }
    }
}
=== app/src/main/java/com/nightadhan/app/PrayerData.kt ===
package com.nightadhan.app

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.util.Calendar

class DayData(val times: LongArray, val hijri: String, val weekday: String)

object PrayerData {
    val KEYS = arrayOf("Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha")
    val NAMES = arrayOf("الفجر", "الشروق", "الظهر", "العصر", "المغرب", "العشاء")
    val ICONS = arrayOf("nights_stay", "wb_twilight", "wb_sunny", "wb_cloudy", "bedtime", "dark_mode")

    val METHOD_IDS = intArrayOf(5, 3, 4, 1, 2, 9, 10, 16, 13, 23, 19, 18, 21)
    val METHOD_NAMES = arrayOf(
        "الهيئة المصرية العامة للمساحة",
        "رابطة العالم الإسلامي",
        "أم القرى (مكة المكرمة)",
        "جامعة العلوم الإسلامية - كراتشي",
        "أمريكا الشمالية (ISNA)",
        "الكويت",
        "قطر",
        "دبي",
        "تركيا (ديانت)",
        "الأردن",
        "الجزائر",
        "تونس",
        "المغرب"
    )

    val DHIKR = arrayOf(
        "اللهم صلِّ على النبي محمد",
        "سبحان الله",
        "الحمد لله",
        "لا إله إلا الله",
        "الله أكبر",
        "أستغفر الله",
        "سبحان الله وبحمده، سبحان الله العظيم",
        "لا حول ولا قوة إلا بالله"
    )
    val DHIKR_KEYS = arrayOf(
        "salawat", "subhanallah", "alhamdulillah", "lailaha",
        "allahuakbar", "istighfar", "tasbih", "hawqala"
    )

    fun hasLocation(c: Context): Boolean {
        val p = c.prefs()
        return if (p.getString("mode", "gps") == "city") {
            !p.getString("city", "").isNullOrEmpty()
        } else {
            p.contains("lat") && p.contains("lon")
        }
    }

    fun coords(c: Context): Pair<Double, Double>? {
        val p = c.prefs()
        val la: String?
        val lo: String?
        if (p.getString("mode", "gps") == "city") {
            la = p.getString("meta_lat", null)
            lo = p.getString("meta_lon", null)
        } else {
            la = p.getString("lat", null)
            lo = p.getString("lon", null)
        }
        val a = la?.toDoubleOrNull()
        val b = lo?.toDoubleOrNull()
        return if (a != null && b != null) Pair(a, b) else null
    }

    private fun cacheKey(p: SharedPreferences): String =
        listOf(
            p.getString("mode", "gps"),
            p.getString("lat", ""),
            p.getString("lon", ""),
            p.getString("city", ""),
            p.getString("country", ""),
            p.getInt("method", 5),
            p.getInt("school", 0)
        ).joinToString("|")

    fun clearCache(c: Context) {
        val p = c.prefs()
        val e = p.edit()
        for (k in p.all.keys) {
            if (k.startsWith("cal_")) e.remove(k)
        }
        e.apply()
    }

    /** Blocking (network). Call from a background thread. */
    fun ensureData(c: Context): Boolean {
        val p = c.prefs()
        if (!hasLocation(c)) return false
        val key = cacheKey(p)
        if (p.getString("cache_key", "") != key) {
            clearCache(c)
            p.edit().putString("cache_key", key).apply()
        }
        val wanted = HashSet<String>()
        var okNow = true
        for (i in 0..1) {
            val cl = Calendar.getInstance()
            cl.set(Calendar.DAY_OF_MONTH, 1)
            cl.add(Calendar.MONTH, i)
            val y = cl.get(Calendar.YEAR)
            val m = cl.get(Calendar.MONTH) + 1
            val k = "cal_" + y + "_" + m
            wanted.add(k)
            if (!p.contains(k)) {
                val json = fetchMonth(c, y, m)
                if (json != null) {
                    p.edit().putString(k, json).apply()
                } else if (i == 0) {
                    okNow = false
                }
            }
        }
        val e2 = p.edit()
        for (k in p.all.keys) {
            if (k.startsWith("cal_") && !wanted.contains(k)) e2.remove(k)
        }
        e2.apply()
        return okNow
    }

    private fun fetchMonth(c: Context, year: Int, month: Int): String? {
        val p = c.prefs()
        val method = p.getInt("method", 5)
        val school = p.getInt("school", 0)
        val url: String = if (p.getString("mode", "gps") == "city") {
            val city = URLEncoder.encode(p.getString("city", "") ?: "", "UTF-8")
            val country = URLEncoder.encode(p.getString("country", "") ?: "", "UTF-8")
            "https://api.aladhan.com/v1/calendarByCity/" + year + "/" + month +
                "?city=" + city + "&country=" + country +
                "&method=" + method + "&school=" + school
        } else {
            "https://api.aladhan.com/v1/calendar/" + year + "/" + month +
                "?latitude=" + p.getString("lat", "0") + "&longitude=" + p.getString("lon", "0") +
                "&method=" + method + "&school=" + school
        }
        return try {
            val conn = URL(url).openConnection() as HttpURLConnection
            conn.connectTimeout = 15000
            conn.readTimeout = 25000
            val body = conn.inputStream.bufferedReader().use { it.readText() }
            conn.disconnect()
            val root = JSONObject(body)
            if (root.optInt("code") != 200) {
                null
            } else {
                val arr = root.getJSONArray("data")
                try {
                    val meta = arr.getJSONObject(0).optJSONObject("meta")
                    if (meta != null) {
                        p.edit()
                            .putString("meta_lat", meta.optString("latitude"))
                            .putString("meta_lon", meta.optString("longitude"))
                            .apply()
                    }
                } catch (e: Exception) {
                    // ignore
                }
                arr.toString()
            }
        } catch (e: Exception) {
            null
        }
    }

    fun dayData(c: Context, cal: Calendar): DayData? {
        val p = c.prefs()
        val y = cal.get(Calendar.YEAR)
        val m = cal.get(Calendar.MONTH) + 1
        val d = cal.get(Calendar.DAY_OF_MONTH)
        val s = p.getString("cal_" + y + "_" + m, null) ?: return null
        return try {
            val arr = JSONArray(s)
            if (d - 1 >= arr.length()) return null
            val o = arr.getJSONObject(d - 1)
            val t = o.getJSONObject("timings")
            val times = LongArray(6)
            for (i in 0 until 6) {
                val raw = t.getString(KEYS[i]).trim()
                val hh = raw.substring(0, 2).toInt()
                val mm = raw.substring(3, 5).toInt()
                val c2 = Calendar.getInstance()
                c2.set(y, m - 1, d, hh, mm, 0)
                c2.set(Calendar.MILLISECOND, 0)
                times[i] = c2.timeInMillis + p.getInt("adj_" + i, 0) * 60000L
            }
            val h = o.getJSONObject("date").getJSONObject("hijri")
            val hijri = h.getString("day") + " " +
                h.getJSONObject("month").getString("ar") + " " +
                h.getString("year") + " هـ"
            val wd = h.getJSONObject("weekday").getString("ar")
            DayData(times, hijri, wd)
        } catch (e: Exception) {
            null
        }
    }
}
=== app/src/main/java/com/nightadhan/app/Scheduler.kt ===
package com.nightadhan.app

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Build
import java.util.Calendar

object Scheduler {
    const val ACTION_EVENT = "com.nightadhan.app.EVENT"
    const val ACTION_DHIKR = "com.nightadhan.app.DHIKR"

    private class Ev(val at: Long, val kind: Int, val prayer: Int)

    private fun am(c: Context) = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
    private fun eventIntent(c: Context) = Intent(c, AlarmReceiver::class.java).setAction(ACTION_EVENT)
    private fun dhikrIntent(c: Context) = Intent(c, DhikrReceiver::class.java).setAction(ACTION_DHIKR)

    private fun setExact(alarm: AlarmManager, t: Long, pi: PendingIntent) {
        try {
            if (Build.VERSION.SDK_INT >= 31 && !alarm.canScheduleExactAlarms()) {
                alarm.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, t, pi)
            } else {
                alarm.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, t, pi)
            }
        } catch (e: Exception) {
            try {
                alarm.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, t, pi)
            } catch (e2: Exception) {
                // ignore
            }
        }
    }

    @Synchronized
    fun scheduleAll(c: Context) {
        val alarm = am(c)
        val p = c.prefs()
        for (k in 0 until 60) {
            val old = PendingIntent.getBroadcast(
                c, 200 + k, eventIntent(c),
                PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
            )
            if (old != null) {
                alarm.cancel(old)
                old.cancel()
            }
        }
        val now = System.currentTimeMillis()
        val preOn = p.getBoolean("pre_on", true)
        val preMin = p.getInt("pre_min", 5)
        val friOn = p.getBoolean("friday_on", false)
        val friMin = p.getInt("friday_min", 60)
        val list = ArrayList<Ev>()
        for (d in 0..2) {
            val cl = Calendar.getInstance()
            cl.add(Calendar.DAY_OF_MONTH, d)
            val dd = PrayerData.dayData(c, cl) ?: continue
            for (i in intArrayOf(0, 2, 3, 4, 5)) {
                val t = dd.times[i]
                if (p.getBoolean("adhan_" + i, true) && t > now) list.add(Ev(t, 0, i))
                if (preOn && p.getBoolean("pre_" + i, true)) {
                    val pt = t - preMin * 60000L
                    if (pt > now) list.add(Ev(pt, 1, i))
                }
            }
            if (friOn && cl.get(Calendar.DAY_OF_WEEK) == Calendar.FRIDAY) {
                val ft = dd.times[2] - friMin * 60000L
                if (ft > now) list.add(Ev(ft, 2, 2))
            }
        }
        list.sortBy { it.at }
        val show = PendingIntent.getActivity(
            c, 0, Intent(c, MainActivity::class.java), PendingIntent.FLAG_IMMUTABLE
        )
        for ((k, ev) in list.take(40).withIndex()) {
            val pi = PendingIntent.getBroadcast(
                c, 200 + k,
                eventIntent(c).putExtra("kind", ev.kind).putExtra("prayer", ev.prayer),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            if (ev.kind == 0) {
                try {
                    alarm.setAlarmClock(AlarmManager.AlarmClockInfo(ev.at, show), pi)
                } catch (e: Exception) {
                    setExact(alarm, ev.at, pi)
                }
            } else {
                setExact(alarm, ev.at, pi)
            }
        }
    }

    fun inQuiet(p: SharedPreferences, hour: Int): Boolean {
        if (!p.getBoolean("quiet_on", false)) return false
        val s = p.getInt("quiet_start", 23)
        val e = p.getInt("quiet_end", 5)
        return if (s <= e) hour in s until e else (hour >= s || hour < e)
    }

    fun cancelDhikr(c: Context) {
        val old = PendingIntent.getBroadcast(
            c, 300, dhikrIntent(c),
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (old != null) {
            am(c).cancel(old)
            old.cancel()
        }
    }

    fun scheduleDhikr(c: Context) {
        cancelDhikr(c)
        val p = c.prefs()
        if (!p.getBoolean("dhikr_on", false)) return
        val interval = p.getInt("dhikr_min", 30)
        var t = System.currentTimeMillis() + interval * 60000L
        val cl = Calendar.getInstance()
        cl.timeInMillis = t
        if (inQuiet(p, cl.get(Calendar.HOUR_OF_DAY))) {
            cl.set(Calendar.MINUTE, 0)
            cl.set(Calendar.SECOND, 0)
            cl.set(Calendar.MILLISECOND, 0)
            var guard = 0
            while (inQuiet(p, cl.get(Calendar.HOUR_OF_DAY)) && guard < 30) {
                cl.add(Calendar.HOUR_OF_DAY, 1)
                guard++
            }
            t = cl.timeInMillis
        }
        val pi = PendingIntent.getBroadcast(
            c, 300, dhikrIntent(c),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        setExact(am(c), t, pi)
    }

    fun pickDhikrIndex(c: Context): Int {
        val sel = (c.prefs().getString("dhikr_sel", "0,1,2") ?: "0")
            .split(",")
            .mapNotNull { it.trim().toIntOrNull() }
            .filter { it in PrayerData.DHIKR.indices }
        return if (sel.isEmpty()) 0 else sel.random()
    }
}
=== app/src/main/java/com/nightadhan/app/Notif.kt ===
package com.nightadhan.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent

object Notif {
    const val CH_ADHAN = "adhan_v2"
    const val CH_PRE = "pre_v2"
    const val CH_DHIKR = "dhikr_v2"

    fun ensure(c: Context) {
        val nm = c.getSystemService(NotificationManager::class.java)
        val a = NotificationChannel(CH_ADHAN, "الأذان", NotificationManager.IMPORTANCE_HIGH).apply {
            description = "إشعار وقت الأذان"
            setSound(null, null)
            enableVibration(false)
            lockscreenVisibility = Notification.VISIBILITY_PUBLIC
        }
        val b = NotificationChannel(CH_PRE, "التنبيه قبل الصلاة", NotificationManager.IMPORTANCE_HIGH).apply {
            description = "تنبيه قبل الصلاة وتذكير الجمعة"
            setSound(null, null)
            enableVibration(false)
            lockscreenVisibility = Notification.VISIBILITY_PUBLIC
        }
        val d = NotificationChannel(CH_DHIKR, "الأذكار الدورية", NotificationManager.IMPORTANCE_DEFAULT).apply {
            description = "تذكير دوري بالأذكار"
            setSound(null, null)
            enableVibration(false)
        }
        nm.createNotificationChannel(a)
        nm.createNotificationChannel(b)
        nm.createNotificationChannel(d)
    }

    fun openApp(c: Context): PendingIntent =
        PendingIntent.getActivity(
            c, 1, Intent(c, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
}
=== app/src/main/java/com/nightadhan/app/Services.kt ===
package com.nightadhan.app

import android.app.Notification
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.os.VibrationEffect
import android.os.Vibrator
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import java.util.Locale

class AdhanService : Service() {

    companion object {
        const val ACTION_STOP = "com.nightadhan.app.STOP_ADHAN"

        @Volatile
        var playing = false
    }

    private var mp: MediaPlayer? = null
    private var kind = 0
    private var prayer = 2
    private var started = false
    private var finished = false
    private var focusReq: AudioFocusRequest? = null
    private val handler = Handler(Looper.getMainLooper())

    private fun nid(): Int = if (kind == 0) 2001 else 2003

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            if (started) finishNow(true) else stopSelf()
            return START_NOT_STICKY
        }
        kind = intent?.getIntExtra("kind", 0) ?: 0
        prayer = intent?.getIntExtra("prayer", 2) ?: 2
        started = true
        finished = false
        playing = kind == 0
        Notif.ensure(this)
        ServiceCompat.startForeground(
            this, nid(), buildNotif(true), ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
        )
        Thread {
            PrayerData.ensureData(this)
            Scheduler.scheduleAll(this)
        }.start()
        if (kind == 0 && prefs().getBoolean("adhan_vibrate", true)) vibrateNow()
        startAudio()
        handler.removeCallbacksAndMessages(null)
        handler.postDelayed({ finishNow(false) }, if (kind == 0) 6 * 60 * 1000L else 45 * 1000L)
        return START_NOT_STICKY
    }

    private fun stopPi(): PendingIntent =
        PendingIntent.getService(
            this, 2,
            Intent(this, AdhanService::class.java).setAction(ACTION_STOP),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

    private fun buildNotif(ongoing: Boolean): Notification {
        val name = PrayerData.NAMES[prayer]
        val title: String
        val text: String
        when (kind) {
            0 -> {
                title = "حان الآن موعد أذان " + name
                text = if (prayer == 0) "الصلاة خير من النوم" else "حان وقت صلاة " + name + "، قم إلى الصلاة"
            }
            1 -> {
                val m = prefs().getInt("pre_min", 5)
                val unit = if (m <= 10) "دقائق" else "دقيقة"
                title = "باقٍ " + arNum(this, m.toString()) + " " + unit + " على أذان " + name
                text = "استعد للصلاة"
            }
            else -> {
                title = "جمعة مباركة"
                text = "لا تنس قراءة سورة الكهف والإكثار من الصلاة على النبي ﷺ"
            }
        }
        val b = NotificationCompat.Builder(this, if (kind == 0) Notif.CH_ADHAN else Notif.CH_PRE)
            .setSmallIcon(R.drawable.ic_stat)
            .setContentTitle(title)
            .setContentText(text)
            .setStyle(NotificationCompat.BigTextStyle().bigText(text))
            .setCategory(if (kind == 0) NotificationCompat.CATEGORY_ALARM else NotificationCompat.CATEGORY_REMINDER)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setContentIntent(Notif.openApp(this))
            .setOngoing(ongoing)
            .setAutoCancel(!ongoing)
        if (ongoing) {
            val stop = stopPi()
            b.addAction(0, "إيقاف", stop)
            b.setDeleteIntent(stop)
        } else if (kind != 0) {
            b.setTimeoutAfter(10 * 60 * 1000L)
        }
        return b.build()
    }

    private fun vibrateNow() {
        try {
            val v = getSystemService(Vibrator::class.java)
            v?.vibrate(VibrationEffect.createWaveform(longArrayOf(0, 500, 250, 500, 250, 500), -1))
        } catch (e: Exception) {
            // ignore
        }
    }

    private fun requestFocus() {
        try {
            val am = getSystemService(AudioManager::class.java)
            val r = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT)
                .setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ALARM)
                        .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                        .build()
                )
                .build()
            am.requestAudioFocus(r)
            focusReq = r
        } catch (e: Exception) {
            // ignore
        }
    }

    private fun abandonFocus() {
        try {
            val r = focusReq
            if (r != null) {
                getSystemService(AudioManager::class.java).abandonAudioFocusRequest(r)
            }
        } catch (e: Exception) {
            // ignore
        }
        focusReq = null
    }

    private fun startAudio() {
        releasePlayer()
        val p = prefs()
        var id: String = if (kind == 0)
            (p.getString("adhan_sound_" + prayer, null) ?: Sounds.defaultAdhan(this, prayer))
        else
            (p.getString("pre_sound", null) ?: Sounds.defaultPre(this))
        if (id == "none") {
            handler.postDelayed({ finishNow(false) }, 2500L)
            return
        }
        if (!Sounds.exists(this, id)) id = "default"
        val usage = if (kind == 0) AudioAttributes.USAGE_ALARM else AudioAttributes.USAGE_NOTIFICATION
        val player = Sounds.createPlayer(this, id, usage, AudioAttributes.CONTENT_TYPE_MUSIC)
        if (player == null) {
            finishNow(false)
            return
        }
        mp = player
        try {
            if (kind == 0) {
                val v = p.getInt("adhan_vol", 100) / 100f
                player.setVolume(v, v)
                requestFocus()
            }
            player.setWakeMode(this, PowerManager.PARTIAL_WAKE_LOCK)
            player.setOnPreparedListener { it.start() }
            player.setOnCompletionListener { finishNow(false) }
            player.setOnErrorListener { _, _, _ ->
                finishNow(false)
                true
            }
            player.prepareAsync()
        } catch (e: Exception) {
            finishNow(false)
        }
    }

    private fun releasePlayer() {
        try {
            mp?.release()
        } catch (e: Exception) {
            // ignore
        }
        mp = null
    }

    private fun finishNow(byUser: Boolean) {
        if (finished) return
        finished = true
        playing = false
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        abandonFocus()
        if (byUser) {
            stopForeground(Service.STOP_FOREGROUND_REMOVE)
        } else {
            stopForeground(Service.STOP_FOREGROUND_DETACH)
            if (started) {
                getSystemService(NotificationManager::class.java).notify(nid(), buildNotif(false))
            }
        }
        stopSelf()
    }

    override fun onDestroy() {
        playing = false
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        abandonFocus()
        super.onDestroy()
    }
}

class DhikrService : Service() {

    private var tts: TextToSpeech? = null
    private var mp: MediaPlayer? = null
    private var done = false
    private val handler = Handler(Looper.getMainLooper())

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        done = false
        Notif.ensure(this)
        val idx = Scheduler.pickDhikrIndex(this)
        val phrase = PrayerData.DHIKR[idx]
        val n = NotificationCompat.Builder(this, Notif.CH_DHIKR)
            .setSmallIcon(R.drawable.ic_stat)
            .setContentTitle("تذكير بالذكر")
            .setContentText(phrase)
            .setStyle(NotificationCompat.BigTextStyle().bigText(phrase))
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setContentIntent(Notif.openApp(this))
            .setAutoCancel(true)
            .setTimeoutAfter(10 * 60 * 1000L)
            .build()
        ServiceCompat.startForeground(
            this, 2002, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
        )
        Scheduler.scheduleDhikr(this)
        handler.removeCallbacksAndMessages(null)
        handler.postDelayed({ finishUp() }, 60000L)
        if (AdhanService.playing) {
            finishUp()
        } else {
            play(idx, phrase)
        }
        return START_NOT_STICKY
    }

    private fun play(idx: Int, phrase: String) {
        var id = prefs().getString("dhikr_sound_" + idx, null) ?: "tts"
        if (id == "random") {
            id = Sounds.randomFor(this, "dhikr_" + PrayerData.DHIKR_KEYS[idx] + "_") ?: "tts"
        }
        when {
            id == "none" -> finishUp()
            id == "tts" -> speak(phrase)
            id == "default" -> beep()
            Sounds.exists(this, id) -> playFile(id, phrase)
            else -> speak(phrase)
        }
    }

    private fun playFile(id: String, phrase: String) {
        val player = Sounds.createPlayer(
            this, id, AudioAttributes.USAGE_NOTIFICATION, AudioAttributes.CONTENT_TYPE_MUSIC
        )
        if (player == null) {
            speak(phrase)
            return
        }
        mp = player
        try {
            player.setOnPreparedListener { it.start() }
            player.setOnCompletionListener { finishUp() }
            player.setOnErrorListener { _, _, _ ->
                finishUp()
                true
            }
            player.prepareAsync()
        } catch (e: Exception) {
            finishUp()
        }
    }

    private fun speak(phrase: String) {
        tts = TextToSpeech(this, TextToSpeech.OnInitListener { status ->
            val t = tts
            if (status != TextToSpeech.SUCCESS || t == null) {
                handler.post { beep() }
                return@OnInitListener
            }
            val r = t.setLanguage(Locale("ar"))
            if (r == TextToSpeech.LANG_MISSING_DATA || r == TextToSpeech.LANG_NOT_SUPPORTED) {
                handler.post { beep() }
                return@OnInitListener
            }
            t.setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            t.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {}
                override fun onDone(utteranceId: String?) {
                    handler.post { finishUp() }
                }

                @Deprecated("Deprecated in Java")
                override fun onError(utteranceId: String?) {
                    handler.post { finishUp() }
                }
            })
            t.speak(phrase, TextToSpeech.QUEUE_FLUSH, null, "dhikr")
        })
    }

    private fun beep() {
        try {
            val r = RingtoneManager.getRingtone(
                this, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            )
            r?.play()
        } catch (e: Exception) {
            // ignore
        }
        handler.postDelayed({ finishUp() }, 4000L)
    }

    private fun finishUp() {
        if (done) return
        done = true
        handler.removeCallbacksAndMessages(null)
        try {
            tts?.stop()
            tts?.shutdown()
        } catch (e: Exception) {
            // ignore
        }
        tts = null
        try {
            mp?.release()
        } catch (e: Exception) {
            // ignore
        }
        mp = null
        stopForeground(Service.STOP_FOREGROUND_DETACH)
        stopSelf()
    }

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        try {
            tts?.shutdown()
        } catch (e: Exception) {
            // ignore
        }
        try {
            mp?.release()
        } catch (e: Exception) {
            // ignore
        }
        super.onDestroy()
    }
}
=== app/src/main/java/com/nightadhan/app/Receivers.kt ===
package com.nightadhan.app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.content.ContextCompat

class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val i = Intent(context, AdhanService::class.java)
            .putExtra("kind", intent.getIntExtra("kind", 0))
            .putExtra("prayer", intent.getIntExtra("prayer", 2))
        ContextCompat.startForegroundService(context, i)
    }
}

class DhikrReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        ContextCompat.startForegroundService(context, Intent(context, DhikrService::class.java))
    }
}

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val app = context.applicationContext
        val pending = goAsync()
        Thread {
            try {
                Scheduler.scheduleAll(app)
                Scheduler.scheduleDhikr(app)
            } finally {
                pending.finish()
            }
            PrayerData.ensureData(app)
            Scheduler.scheduleAll(app)
        }.start()
    }
}
=== app/src/main/java/com/nightadhan/app/Views.kt ===
package com.nightadhan.app

import android.content.Context
import android.content.res.ColorStateList
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.HorizontalScrollView
import android.widget.LinearLayout
import android.widget.SeekBar
import android.widget.Switch
import android.widget.TextView

const val MATCH = ViewGroup.LayoutParams.MATCH_PARENT
const val WRAP = ViewGroup.LayoutParams.WRAP_CONTENT

fun Context.lp(
    w: Int, h: Int, weight: Float = 0f,
    top: Int = 0, bottom: Int = 0, start: Int = 0, end: Int = 0
): LinearLayout.LayoutParams =
    LinearLayout.LayoutParams(w, h, weight).apply {
        topMargin = dp(top)
        bottomMargin = dp(bottom)
        marginStart = dp(start)
        marginEnd = dp(end)
    }

fun Context.hbox(): LinearLayout = LinearLayout(this).apply {
    orientation = LinearLayout.HORIZONTAL
    gravity = Gravity.CENTER_VERTICAL
}

fun Context.vbox(): LinearLayout = LinearLayout(this).apply {
    orientation = LinearLayout.VERTICAL
}

fun Context.pageBox(): LinearLayout = vbox().apply {
    setPadding(dp(16), dp(16), dp(16), dp(28))
}

fun Context.pageTitle(t: String): TextView =
    tv(t, 26f, Night.GOLD, true).apply { setPadding(dp(4), dp(4), dp(4), dp(8)) }

fun Context.sectionTitle(t: String): TextView =
    tv(t, 14f, Night.GOLD, true).apply { setPadding(dp(8), dp(18), dp(8), dp(8)) }

fun Context.pageHeader(title: String, onBack: () -> Unit): LinearLayout {
    val h = hbox().apply {
        setPadding(dp(8), dp(10), dp(16), dp(10))
        setBackgroundColor(Night.BG)
    }
    val back = iconView("arrow_forward", 24f, Night.TEXT).apply {
        setPadding(dp(12), dp(8), dp(12), dp(8))
        setOnClickListener { onBack() }
    }
    h.addView(back)
    h.addView(tv(title, 20f, Night.TEXT, true), lp(0, WRAP, 1f, start = 4))
    return h
}

fun Context.group(vararg rows: View): LinearLayout {
    val g = vbox().apply { background = roundBg(Night.CARD, 18) }
    for ((i, r) in rows.withIndex()) {
        if (i > 0) {
            val line = View(this).apply { setBackgroundColor(Night.CARD2) }
            val lpl = LinearLayout.LayoutParams(MATCH, dp(1))
            lpl.marginStart = dp(56)
            g.addView(line, lpl)
        }
        g.addView(r)
    }
    return g
}

fun Context.settingRow(
    icon: String, title: String, subtitle: String?, onClick: (() -> Unit)?
): LinearLayout {
    val row = hbox().apply { setPadding(dp(16), dp(14), dp(16), dp(14)) }
    row.addView(iconView(icon, 22f, Night.GOLD), LinearLayout.LayoutParams(dp(28), WRAP))
    val col = vbox()
    col.addView(tv(title, 16f, Night.TEXT))
    if (subtitle != null) col.addView(tv(subtitle, 13f, Night.MUTED))
    row.addView(col, lp(0, WRAP, 1f, start = 14))
    if (onClick != null) {
        row.addView(iconView("chevron_left", 22f, Night.MUTED))
        row.setOnClickListener { onClick() }
    }
    return row
}

fun Context.switchRow(
    icon: String, title: String, subtitle: String?, checked: Boolean, onChange: (Boolean) -> Unit
): LinearLayout {
    val row = settingRow(icon, title, subtitle, null)
    val states = arrayOf(intArrayOf(android.R.attr.state_checked), intArrayOf())
    val sw = Switch(this).apply {
        isChecked = checked
        thumbTintList = ColorStateList(states, intArrayOf(Night.GOLD, Night.MUTED))
        trackTintList = ColorStateList(
            states, intArrayOf(alpha(Night.GOLD, 120), alpha(Night.MUTED, 80))
        )
        setOnCheckedChangeListener { _, v -> onChange(v) }
    }
    row.addView(sw)
    row.setOnClickListener { sw.toggle() }
    return row
}

fun Context.chipsRow(options: List<String>, selected: Int, onSelect: (Int) -> Unit): HorizontalScrollView {
    val sv = HorizontalScrollView(this).apply { isHorizontalScrollBarEnabled = false }
    val box = hbox().apply { setPadding(dp(12), dp(8), dp(12), dp(12)) }
    val views = ArrayList<TextView>()
    var sel = selected
    fun paint() {
        for ((i, v) in views.withIndex()) {
            v.background = roundBg(if (i == sel) Night.GOLD else Night.CARD2, 20)
            v.setTextColor(if (i == sel) Night.onGold else Night.TEXT)
        }
    }
    for ((i, o) in options.withIndex()) {
        val chip = tv(o, 14f, Night.TEXT, true).apply {
            setPadding(dp(16), dp(8), dp(16), dp(8))
            setOnClickListener {
                sel = i
                paint()
                onSelect(i)
            }
        }
        views.add(chip)
        box.addView(chip, lp(WRAP, WRAP, end = 8))
    }
    paint()
    sv.addView(box)
    return sv
}

fun Context.stepperRow(
    icon: String, title: String, initial: Int, min: Int, max: Int,
    fmt: (Int) -> String, onChange: (Int) -> Unit
): LinearLayout {
    var v = initial
    val row = hbox().apply { setPadding(dp(16), dp(10), dp(12), dp(10)) }
    row.addView(iconView(icon, 22f, Night.GOLD), LinearLayout.LayoutParams(dp(28), WRAP))
    row.addView(tv(title, 16f, Night.TEXT), lp(0, WRAP, 1f, start = 14))
    val value = tv(fmt(v), 15f, Night.TEXT, true).apply {
        gravity = Gravity.CENTER
        minWidth = dp(84)
    }
    val minus = iconView("remove", 22f, Night.onGold).apply {
        background = roundBg(Night.GOLD, 20)
        setOnClickListener {
            if (v > min) {
                v--
                value.text = fmt(v)
                onChange(v)
            }
        }
    }
    val plus = iconView("add", 22f, Night.onGold).apply {
        background = roundBg(Night.GOLD, 20)
        setOnClickListener {
            if (v < max) {
                v++
                value.text = fmt(v)
                onChange(v)
            }
        }
    }
    row.addView(plus, LinearLayout.LayoutParams(dp(40), dp(40)))
    row.addView(value)
    row.addView(minus, LinearLayout.LayoutParams(dp(40), dp(40)))
    return row
}

fun Context.seekRow(icon: String, title: String, progress: Int, onChange: (Int) -> Unit): LinearLayout {
    val row = vbox().apply { setPadding(dp(16), dp(14), dp(16), dp(10)) }
    val head = hbox()
    head.addView(iconView(icon, 22f, Night.GOLD), LinearLayout.LayoutParams(dp(28), WRAP))
    head.addView(tv(title, 16f, Night.TEXT), lp(0, WRAP, 1f, start = 14))
    val value = tv(arNum(this, progress.toString() + "%"), 14f, Night.MUTED)
    head.addView(value)
    row.addView(head)
    val ctx = this
    val sb = SeekBar(this).apply {
        max = 100
        this.progress = progress
        progressTintList = ColorStateList.valueOf(Night.GOLD)
        thumbTintList = ColorStateList.valueOf(Night.GOLD)
        setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(s: SeekBar?, p: Int, fromUser: Boolean) {
                value.text = arNum(ctx, p.toString() + "%")
                if (fromUser) onChange(p)
            }

            override fun onStartTrackingTouch(s: SeekBar?) {}
            override fun onStopTrackingTouch(s: SeekBar?) {}
        })
    }
    row.addView(sb, lp(MATCH, WRAP, top = 6))
    return row
}

class CompassView(ctx: Context) : View(ctx) {
    var heading = 0f
    var qibla = 0f
    var hasQibla = false
    var aligned = false

    private val ring = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.STROKE }
    private val fill = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
    private val text = Paint(Paint.ANTI_ALIAS_FLAG).apply { textAlign = Paint.Align.CENTER }
    private val iconPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { textAlign = Paint.Align.CENTER }

    private fun d(v: Int): Float = context.dp(v).toFloat()

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val cx = width / 2f
        val cy = height / 2f
        val r = minOf(cx, cy) - d(16)

        fill.color = Night.CARD
        canvas.drawCircle(cx, cy, r + d(10), fill)
        ring.color = if (aligned) Night.GOLD else Night.CARD2
        ring.strokeWidth = if (aligned) d(5) else d(3)
        canvas.drawCircle(cx, cy, r, ring)

        canvas.save()
        canvas.rotate(-heading, cx, cy)

        ring.color = Night.MUTED
        for (a in 0 until 360 step 15) {
            val len = if (a % 90 == 0) d(14) else if (a % 45 == 0) d(10) else d(6)
            ring.strokeWidth = if (a % 90 == 0) d(3) else d(1)
            canvas.save()
            canvas.rotate(a.toFloat(), cx, cy)
            canvas.drawLine(cx, cy - r + d(4), cx, cy - r + d(4) + len, ring)
            canvas.restore()
        }

        val letters = arrayOf("ش", "ق", "ج", "غ")
        text.textSize = d(18)
        for (k in 0..3) {
            canvas.save()
            canvas.rotate(k * 90f, cx, cy)
            text.color = if (k == 0) Night.GOLD else Night.TEXT
            canvas.drawText(letters[k], cx, cy - r + d(40), text)
            canvas.restore()
        }

        if (hasQibla) {
            canvas.save()
            canvas.rotate(qibla, cx, cy)
            ring.color = Night.GOLD
            ring.strokeWidth = d(3)
            canvas.drawLine(cx, cy, cx, cy - r + d(72), ring)
            val f = Icons.face(context)
            if (f != null) {
                iconPaint.typeface = f
                iconPaint.fontFeatureSettings = "'liga'"
                iconPaint.color = Night.GOLD
                iconPaint.textSize = d(34)
                canvas.drawText("mosque", cx, cy - r + d(66), iconPaint)
            } else {
                fill.color = Night.GOLD
                canvas.drawCircle(cx, cy - r + d(60), d(10), fill)
            }
            canvas.restore()
        }
        canvas.restore()

        fill.color = Night.TEXT
        val path = Path()
        path.moveTo(cx, cy - r - d(8))
        path.lineTo(cx - d(9), cy - r + d(12))
        path.lineTo(cx + d(9), cy - r + d(12))
        path.close()
        canvas.drawPath(path, fill)

        fill.color = Night.GOLD
        canvas.drawCircle(cx, cy, d(6), fill)
    }
}
=== app/src/main/java/com/nightadhan/app/MainActivity.kt ===
package com.nightadhan.app

import android.Manifest
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.location.Geocoder
import android.location.Location
import android.location.LocationManager
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.provider.Settings
import android.view.Gravity
import android.view.HapticFeedbackConstants
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.core.location.LocationManagerCompat
import androidx.core.view.WindowCompat
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

class MainActivity : ComponentActivity() {

    companion object {
        var splashDone = false
    }

    private val handler = Handler(Looper.getMainLooper())
    private val splashT0 = SystemClock.uptimeMillis()

    private lateinit var pageHost: FrameLayout
    private lateinit var nav: LinearLayout
    private var splash: FrameLayout? = null
    private lateinit var homeView: ScrollView
    private var tab = 0
    private val stack = ArrayList<Pair<String, () -> View>>()

    private val navItems = arrayOf(
        Pair("home", "الرئيسية"),
        Pair("touch_app", "الأذكار"),
        Pair("explore", "القبلة"),
        Pair("settings", "الإعدادات")
    )
    private val navIcons = ArrayList<TextView>()
    private val navLabels = ArrayList<TextView>()

    // home widgets
    private lateinit var placeText: TextView
    private lateinit var dateText: TextView
    private lateinit var hijriText: TextView
    private lateinit var nextLabel: TextView
    private lateinit var nextIcon: TextView
    private lateinit var nextName: TextView
    private lateinit var nextTime: TextView
    private lateinit var countdown: TextView
    private lateinit var progress: ProgressBar
    private lateinit var rowsBox: LinearLayout
    private lateinit var statusText: TextView
    private lateinit var notifBanner: View
    private var nextIdx = 2
    private var nextAt = 0L
    private var prevAt = 0L

    // sound preview
    private var preview: MediaPlayer? = null
    private var previewId: String? = null
    private val previewIcons = HashMap<String, TextView>()

    // qibla
    private var compass: CompassView? = null
    private var qiblaInfo: TextView? = null
    private var qiblaBearing = Double.NaN
    private var smoothed = 0f
    private var sensorOn = false

    private val tick = object : Runnable {
        override fun run() {
            updateCountdown()
            handler.postDelayed(this, 1000)
        }
    }

    private val notifLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { updateBanner() }

    private val locPermLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { res ->
            if (res.values.any { it }) useGps() else toast("بدون إذن الموقع اختر المدينة يدويًا")
        }

    private val customPicker =
        registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
            if (uri != null) {
                Thread {
                    val ok = Sounds.addCustomBlocking(this, uri)
                    runOnUiThread {
                        toast(if (ok) "تمت إضافة الصوت" else "تعذر إضافة الملف")
                        if (stack.isNotEmpty()) showSub()
                    }
                }.start()
            }
        }

    private val sensorListener = object : SensorEventListener {
        private val rot = FloatArray(9)
        private val ori = FloatArray(3)

        override fun onSensorChanged(e: SensorEvent) {
            try {
                val v = if (e.values.size > 4) e.values.copyOfRange(0, 4) else e.values
                SensorManager.getRotationMatrixFromVector(rot, v)
                SensorManager.getOrientation(rot, ori)
                var az = Math.toDegrees(ori[0].toDouble()).toFloat()
                if (az < 0) az += 360f
                val diff = ((az - smoothed + 540f) % 360f) - 180f
                smoothed = (smoothed + diff * 0.15f + 360f) % 360f
                val cv = compass ?: return
                cv.heading = smoothed
                if (!qiblaBearing.isNaN()) {
                    val dq = ((smoothed - qiblaBearing.toFloat() + 540f) % 360f) - 180f
                    cv.aligned = Math.abs(dq) < 5f
                    qiblaInfo?.text = if (cv.aligned) "أنت تواجه القبلة الآن"
                    else "اتجاه القبلة: " + arNum(this@MainActivity, qiblaBearing.toInt().toString()) +
                        " درجة من الشمال"
                }
                cv.invalidate()
            } catch (ex: Exception) {
                // ignore
            }
        }

        override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
    }

    // ------------------------------------------------------------ lifecycle

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Night.apply(prefs().getInt("theme", 0))
        window.statusBarColor = Night.BG
        window.navigationBarColor = Night.CARD
        val ic = WindowCompat.getInsetsController(window, window.decorView)
        ic.isAppearanceLightStatusBars = Night.light
        ic.isAppearanceLightNavigationBars = Night.light
        Notif.ensure(this)

        val root = FrameLayout(this).apply {
            setBackgroundColor(Night.BG)
            layoutDirection = View.LAYOUT_DIRECTION_RTL
        }
        val column = vbox()
        pageHost = FrameLayout(this)
        column.addView(pageHost, lp(MATCH, 0, 1f))
        nav = buildNav()
        column.addView(nav, lp(MATCH, WRAP))
        root.addView(column, FrameLayout.LayoutParams(MATCH, MATCH))
        homeView = buildHome()
        if (!splashDone) {
            val s = buildSplash()
            splash = s
            root.addView(s, FrameLayout.LayoutParams(MATCH, MATCH))
            handler.postDelayed({ hideSplash() }, 8000L)
        }
        setContentView(root)
        showTab(0)

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (stack.isNotEmpty()) {
                    popSub()
                } else if (tab != 0) {
                    showTab(0)
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED
        ) {
            notifLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
        if (!PrayerData.hasLocation(this)) {
            splashReady()
            handler.postDelayed({ locationChoice() }, 2100L)
        }
    }

    override fun onResume() {
        super.onResume()
        render()
        updateBanner()
        handler.removeCallbacks(tick)
        handler.post(tick)
        if (PrayerData.hasLocation(this)) reload()
        updateSensor()
    }

    override fun onPause() {
        super.onPause()
        handler.removeCallbacks(tick)
        stopPreview()
        stopSensor()
    }

    // ------------------------------------------------------------ splash

    private fun buildSplash(): FrameLayout {
        val f = FrameLayout(this).apply {
            background = GradientDrawable(
                GradientDrawable.Orientation.TOP_BOTTOM,
                intArrayOf(Night.SPLASH_BG, Night.SPLASH_BG2)
            )
            isClickable = true
        }
        val col = vbox().apply { gravity = Gravity.CENTER_HORIZONTAL }
        val circle = FrameLayout(this).apply {
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(Color.parseColor("#1D2742"))
                setStroke(dp(2), Night.HEROGOLD)
            }
        }
        circle.addView(
            iconView("mosque", 64f, Night.HEROGOLD),
            FrameLayout.LayoutParams(WRAP, WRAP, Gravity.CENTER)
        )
        col.addView(circle, LinearLayout.LayoutParams(dp(132), dp(132)))
        col.addView(tv("مؤذن", 36f, Night.HEROGOLD, true), lp(WRAP, WRAP, top = 22))
        col.addView(tv("مواقيت الصلاة والأذان", 15f, Night.HEROMUTED), lp(WRAP, WRAP, top = 4))
        val bar = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            isIndeterminate = true
            indeterminateTintList = ColorStateList.valueOf(Night.HEROGOLD)
        }
        col.addView(bar, lp(dp(160), dp(4), top = 36))
        col.addView(tv("جاري تجهيز المواقيت...", 13f, Night.HEROMUTED), lp(WRAP, WRAP, top = 12))
        f.addView(col, FrameLayout.LayoutParams(WRAP, WRAP, Gravity.CENTER))
        return f
    }

    private fun hideSplash() {
        val s = splash ?: return
        splash = null
        splashDone = true
        s.animate().alpha(0f).setDuration(420L).withEndAction {
            (s.parent as? ViewGroup)?.removeView(s)
        }.start()
    }

    private fun splashReady() {
        if (splash == null) return
        val wait = (1700L - (SystemClock.uptimeMillis() - splashT0)).coerceAtLeast(0L)
        handler.postDelayed({ hideSplash() }, wait)
    }

    // ------------------------------------------------------------ navigation

    private fun buildNav(): LinearLayout {
        val n = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setBackgroundColor(Night.CARD)
            setPadding(0, dp(4), 0, dp(4))
        }
        for ((i, item) in navItems.withIndex()) {
            val cell = vbox().apply {
                gravity = Gravity.CENTER
                setPadding(0, dp(8), 0, dp(8))
                setOnClickListener { showTab(i) }
            }
            val ic = iconView(item.first, 24f, Night.MUTED)
            val lb = tv(item.second, 11f, Night.MUTED)
            cell.addView(ic)
            cell.addView(lb)
            navIcons.add(ic)
            navLabels.add(lb)
            n.addView(cell, lp(0, WRAP, 1f))
        }
        return n
    }

    private fun scrollPage(content: View): ScrollView =
        ScrollView(this).apply {
            setBackgroundColor(Night.BG)
            isVerticalScrollBarEnabled = false
            addView(content)
        }

    private fun showTab(i: Int) {
        stopPreview()
        stack.clear()
        tab = i
        nav.visibility = View.VISIBLE
        pageHost.removeAllViews()
        val v: View = when (i) {
            0 -> homeView
            1 -> scrollPage(buildAzkar())
            2 -> scrollPage(buildQibla())
            else -> scrollPage(buildSettings())
        }
        pageHost.addView(v, FrameLayout.LayoutParams(MATCH, MATCH))
        for (k in navIcons.indices) {
            val c = if (k == i) Night.GOLD else Night.MUTED
            navIcons[k].setTextColor(c)
            navLabels[k].setTextColor(c)
        }
        updateSensor()
    }

    private fun openSub(title: String, builder: () -> View) {
        stack.add(Pair(title, builder))
        showSub()
    }

    private fun showSub() {
        val top = stack[stack.size - 1]
        nav.visibility = View.GONE
        pageHost.removeAllViews()
        val col = vbox().apply { setBackgroundColor(Night.BG) }
        col.addView(pageHeader(top.first) { popSub() })
        col.addView(scrollPage(top.second()), lp(MATCH, 0, 1f))
        pageHost.addView(col, FrameLayout.LayoutParams(MATCH, MATCH))
        updateSensor()
    }

    private fun popSub() {
        stopPreview()
        if (stack.isNotEmpty()) stack.removeAt(stack.size - 1)
        if (stack.isEmpty()) showTab(tab) else showSub()
    }

    // ------------------------------------------------------------ home

    private fun buildHome(): ScrollView {
        val content = pageBox()

        val top = hbox()
        top.addView(iconView("mosque", 26f, Night.GOLD))
        top.addView(tv("مؤذن", 24f, Night.GOLD, true), lp(0, WRAP, 1f, start = 10))
        val refreshBtn = iconView("refresh", 24f, Night.TEXT).apply {
            setPadding(dp(10), dp(6), dp(10), dp(6))
            setOnClickListener { forceReload() }
        }
        top.addView(refreshBtn)
        content.addView(top)

        notifBanner = group(
            settingRow(
                "notifications_off", "الإشعارات متوقفة",
                "اضغط لتفعيلها حتى يصلك الأذان والتنبيهات"
            ) { openNotifSettings() }
        )
        notifBanner.visibility = View.GONE
        content.addView(notifBanner, lp(MATCH, WRAP, top = 12))

        val placeRow = hbox().apply { setPadding(0, dp(12), 0, 0) }
        placeRow.addView(iconView("location_on", 18f, Night.TEAL))
        placeText = tv("", 14f, Night.MUTED)
        placeRow.addView(placeText, lp(0, WRAP, 1f, start = 6))
        content.addView(placeRow)
        dateText = tv("", 15f, Night.TEXT)
        content.addView(dateText, lp(WRAP, WRAP, top = 4))
        hijriText = tv("", 15f, Night.TEAL)
        content.addView(hijriText, lp(WRAP, WRAP, bottom = 14))

        val hero = vbox().apply {
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(20), dp(24), dp(20), dp(24))
            background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(Night.HERO1, Night.HERO2)
            ).apply { cornerRadius = dp(26).toFloat() }
        }
        nextLabel = tv("", 14f, Night.HEROGOLD)
        nextIcon = iconView("", 32f, Night.HEROGOLD)
        nextName = tv("", 34f, Night.HEROTEXT, true)
        val nameRow = hbox().apply { gravity = Gravity.CENTER }
        nameRow.addView(nextIcon)
        nameRow.addView(nextName, lp(WRAP, WRAP, start = 10))
        nextTime = tv("", 18f, Night.HEROMUTED)
        countdown = tv("", 44f, Night.HEROGOLD, true)
        countdown.typeface = Typeface.MONOSPACE
        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 1000
            progressTintList = ColorStateList.valueOf(Night.HEROGOLD)
            progressBackgroundTintList = ColorStateList.valueOf(Color.parseColor("#33FFFFFF"))
        }
        hero.addView(nextLabel)
        hero.addView(nameRow, lp(WRAP, WRAP, top = 6))
        hero.addView(nextTime, lp(WRAP, WRAP, top = 2))
        hero.addView(countdown, lp(WRAP, WRAP, top = 10, bottom = 10))
        hero.addView(progress, LinearLayout.LayoutParams(MATCH, dp(8)))
        content.addView(hero)

        rowsBox = vbox().apply {
            setPadding(dp(6), dp(6), dp(6), dp(6))
            background = roundBg(Night.CARD, 20)
        }
        content.addView(rowsBox, lp(MATCH, WRAP, top = 16))

        content.addView(
            group(
                settingRow("my_location", "تحديث الموقع", "GPS أو إدخال المدينة") { locationChoice() }
            ),
            lp(MATCH, WRAP, top = 16)
        )

        statusText = tv("", 13f, Night.MUTED)
        statusText.gravity = Gravity.CENTER
        content.addView(statusText, lp(MATCH, WRAP, top = 12))
        return scrollPage(content)
    }

    private fun render() {
        val p = prefs()
        var place = p.getString("place", "") ?: ""
        if (place.isEmpty() && p.contains("lat")) {
            place = p.getString("lat", "") + ", " + p.getString("lon", "")
        }
        placeText.text = place.ifEmpty { "حدّد موقعك" }
        val now = System.currentTimeMillis()
        val cal = Calendar.getInstance()
        val today = PrayerData.dayData(this, cal)
        dateText.text = arNum(
            this, SimpleDateFormat("EEEE، d MMMM yyyy", Locale("ar")).format(cal.time)
        )
        rowsBox.removeAllViews()
        if (today == null) {
            hijriText.text = ""
            nextAt = 0L
            nextLabel.text = ""
            nextTime.text = ""
            countdown.text = ""
            progress.progress = 0
            nextIcon.setIcon("")
            nextName.text = if (PrayerData.hasLocation(this)) "جاري التحميل..." else "حدّد موقعك"
            return
        }
        hijriText.text = arNum(this, today.weekday + "، " + today.hijri)

        var idx = -1
        for (i in 0 until 6) {
            if (today.times[i] > now) {
                idx = i
                break
            }
        }
        if (idx >= 0) {
            nextIdx = idx
            nextAt = today.times[idx]
            if (idx > 0) {
                prevAt = today.times[idx - 1]
            } else {
                val y = Calendar.getInstance()
                y.add(Calendar.DAY_OF_MONTH, -1)
                prevAt = PrayerData.dayData(this, y)?.times?.get(5) ?: (today.times[0] - 8 * 3600000L)
            }
        } else {
            val t = Calendar.getInstance()
            t.add(Calendar.DAY_OF_MONTH, 1)
            nextIdx = 0
            nextAt = PrayerData.dayData(this, t)?.times?.get(0) ?: (today.times[0] + 24 * 3600000L)
            prevAt = today.times[5]
        }
        nextLabel.text = if (nextIdx == 1) "الشروق بعد" else "الصلاة القادمة"
        nextIcon.setIcon(PrayerData.ICONS[nextIdx])
        nextName.text = PrayerData.NAMES[nextIdx]
        nextTime.text = clockText(this, nextAt)

        for (i in 0 until 6) {
            val isNext = i == nextIdx
            val passed = today.times[i] <= now && !isNext
            val row = hbox().apply {
                setPadding(dp(14), dp(14), dp(14), dp(14))
                if (isNext) background = roundBg(Night.CARD2, 14)
            }
            val col = if (passed) Night.MUTED else Night.TEXT
            val hi = if (isNext) Night.GOLD else col
            row.addView(iconView(PrayerData.ICONS[i], 22f, hi), LinearLayout.LayoutParams(dp(28), WRAP))
            row.addView(tv(PrayerData.NAMES[i], 18f, hi, isNext), lp(0, WRAP, 1f, start = 12))
            row.addView(tv(clockText(this, today.times[i]), 18f, hi, isNext))
            if (i != 1) {
                val on = prefs().getBoolean("adhan_" + i, true)
                val bell = iconView(
                    if (on) "notifications_active" else "notifications_off", 22f,
                    if (on) Night.GOLD else Night.MUTED
                ).apply {
                    setPadding(dp(14), dp(4), dp(4), dp(4))
                    setOnClickListener {
                        val nv = !prefs().getBoolean("adhan_" + i, true)
                        prefs().edit().putBoolean("adhan_" + i, nv).apply()
                        Thread { Scheduler.scheduleAll(this@MainActivity) }.start()
                        toast(
                            if (nv) "تم تفعيل أذان " + PrayerData.NAMES[i]
                            else "تم إيقاف أذان " + PrayerData.NAMES[i]
                        )
                        render()
                    }
                }
                row.addView(bell)
            } else {
                row.addView(View(this), LinearLayout.LayoutParams(dp(40), dp(1)))
            }
            rowsBox.addView(row)
        }
        updateCountdown()
    }

    private fun updateCountdown() {
        if (nextAt == 0L) return
        val now = System.currentTimeMillis()
        if (now >= nextAt) {
            render()
            return
        }
        countdown.text = countdownText(this, nextAt - now)
        val span = (nextAt - prevAt).coerceAtLeast(1L)
        progress.progress = (((now - prevAt).toDouble() / span) * 1000).toInt().coerceIn(0, 1000)
    }

    private fun updateBanner() {
        if (!::notifBanner.isInitialized) return
        val enabled = NotificationManagerCompat.from(this).areNotificationsEnabled()
        notifBanner.visibility = if (enabled) View.GONE else View.VISIBLE
    }

    private fun openNotifSettings() {
        try {
            startActivity(
                Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                    .putExtra(Settings.EXTRA_APP_PACKAGE, packageName)
            )
        } catch (e: Exception) {
            toast("افتح إعدادات الهاتف وفعّل إشعارات التطبيق")
        }
    }

    // ------------------------------------------------------------ data

    private fun reload() {
        statusText.text = "جاري تحديث المواقيت..."
        Thread {
            val ok = PrayerData.ensureData(this)
            Scheduler.scheduleAll(this)
            runOnUiThread {
                statusText.text = if (ok) "" else "تعذر جلب المواقيت، تأكد من الإنترنت"
                render()
                splashReady()
            }
        }.start()
    }

    private fun forceReload() {
        PrayerData.clearCache(this)
        prefs().edit().remove("cache_key").apply()
        reload()
    }

    // ------------------------------------------------------------ location

    private fun choose(title: String, items: Array<String>, selected: Int, onPick: (Int) -> Unit) {
        AlertDialog.Builder(this)
            .setTitle(title)
            .setSingleChoiceItems(items, selected) { d, i ->
                d.dismiss()
                onPick(i)
            }.show()
    }

    private fun locationChoice() {
        val items = arrayOf("تحديد موقعي تلقائيًا (GPS)", "إدخال المدينة يدويًا")
        AlertDialog.Builder(this)
            .setTitle("تحديد الموقع")
            .setItems(items) { _, i ->
                if (i == 0) useGps() else cityDialog()
            }.show()
    }

    private fun cityDialog() {
        val box = vbox().apply { setPadding(dp(20), dp(10), dp(20), 0) }
        val city = EditText(this).apply {
            hint = "المدينة بالإنجليزية (مثال: Cairo)"
            setSingleLine()
        }
        val country = EditText(this).apply {
            hint = "الدولة بالإنجليزية (مثال: Egypt)"
            setSingleLine()
        }
        box.addView(city)
        box.addView(country)
        AlertDialog.Builder(this)
            .setTitle("المدينة")
            .setView(box)
            .setPositiveButton("حفظ") { _, _ ->
                val c1 = city.text.toString().trim()
                val c2 = country.text.toString().trim()
                if (c1.isNotEmpty() && c2.isNotEmpty()) {
                    prefs().edit()
                        .putString("mode", "city")
                        .putString("city", c1)
                        .putString("country", c2)
                        .putString("place", c1 + "، " + c2)
                        .apply()
                    reload()
                    if (tab == 3 && stack.isEmpty()) showTab(3)
                } else {
                    toast("اكتب المدينة والدولة")
                }
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun useGps() {
        val fine = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED
        val coarse = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED
        if (!fine && !coarse) {
            locPermLauncher.launch(
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION)
            )
            return
        }
        val lm = getSystemService(LOCATION_SERVICE) as LocationManager
        val providers = lm.getProviders(true)
        var best: Location? = null
        for (pr in providers) {
            val l = try {
                lm.getLastKnownLocation(pr)
            } catch (e: SecurityException) {
                null
            }
            if (l != null && (best == null || l.time > best.time)) best = l
        }
        val fallback = best
        if (fallback != null && System.currentTimeMillis() - fallback.time < 6 * 3600000L) {
            onLocation(fallback)
            return
        }
        val provider = when {
            providers.contains(LocationManager.NETWORK_PROVIDER) -> LocationManager.NETWORK_PROVIDER
            providers.contains(LocationManager.GPS_PROVIDER) -> LocationManager.GPS_PROVIDER
            else -> null
        }
        if (provider == null) {
            if (fallback != null) {
                onLocation(fallback)
            } else {
                toast("فعّل خدمة الموقع (GPS) من إعدادات الهاتف ثم أعد المحاولة")
            }
            return
        }
        statusText.text = "جاري تحديد موقعك..."
        try {
            LocationManagerCompat.getCurrentLocation(
                lm, provider, android.os.CancellationSignal(), ContextCompat.getMainExecutor(this),
                androidx.core.util.Consumer<Location?> { loc ->
                    if (loc != null) {
                        onLocation(loc)
                    } else if (fallback != null) {
                        onLocation(fallback)
                    } else {
                        statusText.text = ""
                        toast("تعذر تحديد الموقع، جرّب إدخال المدينة يدويًا")
                    }
                }
            )
        } catch (e: SecurityException) {
            toast("لا يوجد إذن للموقع")
        }
    }

    private fun onLocation(loc: Location) {
        val p = prefs()
        p.edit()
            .putString("mode", "gps")
            .putString("lat", String.format(Locale.US, "%.4f", loc.latitude))
            .putString("lon", String.format(Locale.US, "%.4f", loc.longitude))
            .putString("place", "موقعي الحالي")
            .apply()
        Thread {
            var name: String? = null
            try {
                if (Geocoder.isPresent()) {
                    val l = Geocoder(this, Locale("ar")).getFromLocation(loc.latitude, loc.longitude, 1)
                    if (l != null && l.isNotEmpty()) {
                        val a = l[0]
                        name = listOfNotNull(a.locality ?: a.subAdminArea, a.countryName).joinToString("، ")
                    }
                }
            } catch (e: Exception) {
                // ignore
            }
            if (!name.isNullOrEmpty()) p.edit().putString("place", name).apply()
            runOnUiThread {
                reload()
                if (tab == 3 && stack.isEmpty()) showTab(3)
            }
        }.start()
    }

    // ------------------------------------------------------------ settings

    private fun placeLabel(): String {
        val p = prefs()
        val s = p.getString("place", "") ?: ""
        return if (s.isEmpty()) "غير محدد" else s
    }

    private fun buildSettings(): LinearLayout {
        val p = prefs()
        val c = pageBox()
        c.addView(pageTitle("الإعدادات"))

        c.addView(sectionTitle("الموقع والمواقيت"))
        val methodName = PrayerData.METHOD_NAMES[
            PrayerData.METHOD_IDS.indexOf(p.getInt("method", 5)).coerceAtLeast(0)
        ]
        c.addView(
            group(
                settingRow("location_on", "الموقع", placeLabel()) { locationChoice() },
                settingRow("tune", "طريقة الحساب", methodName) { methodDialog() },
                settingRow(
                    "wb_sunny", "حساب وقت العصر",
                    if (p.getInt("school", 0) == 0) "الجمهور (شافعي / مالكي / حنبلي)" else "حنفي"
                ) { schoolDialog() },
                settingRow("schedule", "تعديل دقائق الصلوات", "تقديم أو تأخير كل صلاة") {
                    openSub("تعديل الدقائق") { buildAdjust() }
                },
                switchRow("access_time", "نظام 24 ساعة", null, p.getBoolean("h24", false)) { v ->
                    p.edit().putBoolean("h24", v).apply()
                    render()
                },
                switchRow("language", "الأرقام العربية", null, p.getBoolean("ar_digits", true)) { v ->
                    p.edit().putBoolean("ar_digits", v).apply()
                    render()
                }
            )
        )

        c.addView(sectionTitle("الأذان والتنبيهات"))
        c.addView(
            group(
                settingRow("notifications_active", "الصلوات والأصوات", "تفعيل الأذان واختيار صوت لكل صلاة") {
                    openSub("الصلوات والأصوات") { buildPrayersPage() }
                },
                settingRow("timer", "التنبيه قبل الصلاة وتذكير الجمعة", null) {
                    openSub("التنبيهات") { buildAlertsPage() }
                },
                seekRow("volume_up", "مستوى صوت الأذان", p.getInt("adhan_vol", 100)) { v ->
                    p.edit().putInt("adhan_vol", v).apply()
                },
                switchRow("vibration", "الاهتزاز مع الأذان", null, p.getBoolean("adhan_vibrate", true)) { v ->
                    p.edit().putBoolean("adhan_vibrate", v).apply()
                },
                settingRow("play_arrow", "تجربة الأذان الآن", "يمكن إيقافه بمسح الإشعار") {
                    testService(0)
                }
            )
        )

        c.addView(sectionTitle("الأذكار"))
        c.addView(
            group(
                settingRow("touch_app", "التذكير الدوري والسبحة", "الأذكار والأصوات وساعات الهدوء") {
                    showTab(1)
                }
            )
        )

        c.addView(sectionTitle("المظهر"))
        c.addView(
            group(
                chipsRow(listOf("ليلي", "أسود داكن", "فاتح"), p.getInt("theme", 0)) { i ->
                    p.edit().putInt("theme", i).apply()
                    recreate()
                }
            )
        )

        c.addView(sectionTitle("النظام"))
        c.addView(
            group(
                settingRow("battery_charging_full", "ضمان عمل التنبيهات", "البطارية والتشغيل التلقائي") {
                    batteryHelp()
                },
                settingRow("refresh", "تحديث المواقيت الآن", null) { forceReload() }
            )
        )
        val foot = tv("مؤذن - الإصدار 2.0", 12f, Night.MUTED)
        foot.gravity = Gravity.CENTER
        c.addView(foot, lp(MATCH, WRAP, top = 20))
        return c
    }

    private fun testService(kind: Int) {
        ContextCompat.startForegroundService(
            this,
            Intent(this, AdhanService::class.java).putExtra("kind", kind).putExtra("prayer", 2)
        )
    }

    private fun methodDialog() {
        val cur = PrayerData.METHOD_IDS.indexOf(prefs().getInt("method", 5)).coerceAtLeast(0)
        choose("طريقة الحساب", PrayerData.METHOD_NAMES, cur) { i ->
            prefs().edit().putInt("method", PrayerData.METHOD_IDS[i]).apply()
            reload()
            showTab(3)
        }
    }

    private fun schoolDialog() {
        val names = arrayOf("الجمهور (شافعي / مالكي / حنبلي)", "حنفي")
        choose("حساب وقت العصر", names, prefs().getInt("school", 0)) { i ->
            prefs().edit().putInt("school", i).apply()
            reload()
            showTab(3)
        }
    }

    private fun batteryHelp() {
        AlertDialog.Builder(this)
            .setTitle("ضمان عمل الأذان")
            .setMessage(
                "حتى يعمل الأذان والتذكير والشاشة مغلقة:\n\n" +
                    "1) اختر «بدون قيود» للبطارية لهذا التطبيق.\n" +
                    "2) فعّل «التشغيل التلقائي / Autostart» (هواتف شاومي وغيرها).\n" +
                    "3) اسمح بالإشعارات."
            )
            .setPositiveButton("إعدادات التطبيق") { _, _ ->
                try {
                    startActivity(
                        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                            .setData(Uri.parse("package:" + packageName))
                    )
                } catch (e: Exception) {
                    toast("افتح الإعدادات ثم التطبيقات ثم مؤذن")
                }
            }
            .setNeutralButton("إعدادات البطارية") { _, _ ->
                try {
                    startActivity(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))
                } catch (e: Exception) {
                    toast("افتح إعدادات البطارية يدويًا")
                }
            }
            .setNegativeButton("إغلاق", null)
            .show()
    }

    private fun buildAdjust(): LinearLayout {
        val p = prefs()
        val c = pageBox()
        c.addView(
            tv(
                "قدّم أو أخّر وقت كل صلاة بالدقائق إذا اختلفت المواقيت عن مسجدك.",
                14f, Night.MUTED
            ), lp(MATCH, WRAP, bottom = 8)
        )
        val rows = ArrayList<View>()
        for (i in intArrayOf(0, 2, 3, 4, 5)) {
            rows.add(
                stepperRow(
                    PrayerData.ICONS[i], PrayerData.NAMES[i], p.getInt("adj_" + i, 0), -30, 30,
                    { v ->
                        val s = if (v > 0) "+" + v else v.toString()
                        arNum(this, s + " د")
                    }
                ) { v ->
                    p.edit().putInt("adj_" + i, v).apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                }
            )
        }
        c.addView(group(*rows.toTypedArray()))
        c.addView(
            group(
                settingRow("restart_alt", "إعادة الضبط", "إلغاء كل التعديلات") {
                    val e = p.edit()
                    for (i in intArrayOf(0, 2, 3, 4, 5)) e.remove("adj_" + i)
                    e.apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                    showSub()
                }
            ),
            lp(MATCH, WRAP, top = 16)
        )
        return c
    }

    private fun buildPrayersPage(): LinearLayout {
        val p = prefs()
        val c = pageBox()
        for (i in intArrayOf(0, 2, 3, 4, 5)) {
            c.addView(sectionTitle(PrayerData.NAMES[i]))
            val cur = p.getString("adhan_sound_" + i, null) ?: Sounds.defaultAdhan(this, i)
            val cats = if (i == 0) listOf("fajr", "adhan") else listOf("adhan")
            c.addView(
                group(
                    switchRow("notifications_active", "تشغيل الأذان", null, p.getBoolean("adhan_" + i, true)) { v ->
                        p.edit().putBoolean("adhan_" + i, v).apply()
                        Thread { Scheduler.scheduleAll(this) }.start()
                    },
                    settingRow("music_note", "صوت الأذان", Sounds.labelOf(this, cur)) {
                        openSub("صوت أذان " + PrayerData.NAMES[i]) {
                            soundPicker(
                                "adhan_sound_" + i, { s -> s.category in cats },
                                tts = false, none = false, random = false,
                                fallback = Sounds.defaultAdhan(this, i)
                            )
                        }
                    },
                    switchRow("timer", "تنبيه قبل الصلاة", null, p.getBoolean("pre_" + i, true)) { v ->
                        p.edit().putBoolean("pre_" + i, v).apply()
                        Thread { Scheduler.scheduleAll(this) }.start()
                    }
                )
            )
        }
        return c
    }

    private fun buildAlertsPage(): LinearLayout {
        val p = prefs()
        val c = pageBox()
        c.addView(sectionTitle("قبل الصلاة"))
        val mins = intArrayOf(5, 10, 15, 20, 30)
        val minLabels = mins.map { arNum(this, it.toString() + " دقيقة") }
        val curPre = p.getString("pre_sound", null) ?: Sounds.defaultPre(this)
        c.addView(
            group(
                switchRow("timer", "تفعيل التنبيه قبل الصلاة", null, p.getBoolean("pre_on", true)) { v ->
                    p.edit().putBoolean("pre_on", v).apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                },
                chipsRow(minLabels, mins.indexOf(p.getInt("pre_min", 5)).coerceAtLeast(0)) { i ->
                    p.edit().putInt("pre_min", mins[i]).apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                },
                settingRow("music_note", "صوت التنبيه", Sounds.labelOf(this, curPre)) {
                    openSub("صوت التنبيه") {
                        soundPicker(
                            "pre_sound", { s -> s.category == "pre" || s.category == "tone" },
                            tts = false, none = true, random = false,
                            fallback = Sounds.defaultPre(this)
                        )
                    }
                },
                settingRow("play_arrow", "تجربة التنبيه الآن", null) { testService(1) }
            )
        )
        c.addView(sectionTitle("يوم الجمعة"))
        val fm = intArrayOf(30, 60, 120)
        val fmLabels = listOf("نصف ساعة", "ساعة", "ساعتان")
        c.addView(
            group(
                switchRow(
                    "event", "تذكير الجمعة", "سورة الكهف والصلاة على النبي قبل الظهر",
                    p.getBoolean("friday_on", false)
                ) { v ->
                    p.edit().putBoolean("friday_on", v).apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                },
                chipsRow(fmLabels, fm.indexOf(p.getInt("friday_min", 60)).coerceAtLeast(0)) { i ->
                    p.edit().putInt("friday_min", fm[i]).apply()
                    Thread { Scheduler.scheduleAll(this) }.start()
                },
                settingRow("play_arrow", "تجربة تذكير الجمعة", null) { testService(2) }
            )
        )
        c.addView(
            tv("وقت التذكير يكون قبل أذان الظهر يوم الجمعة بالمدة المختارة.", 13f, Night.MUTED),
            lp(MATCH, WRAP, top = 8)
        )
        return c
    }

    // ------------------------------------------------------------ sound picker

    private fun soundPicker(
        key: String, filter: (SoundItem) -> Boolean,
        tts: Boolean, none: Boolean, random: Boolean, fallback: String
    ): LinearLayout {
        previewIcons.clear()
        val p = prefs()
        val cur = p.getString(key, null) ?: fallback
        val c = pageBox()
        val rows = ArrayList<View>()
        rows.add(soundRow(key, "default", "نغمة النظام", null, cur == "default"))
        if (none) rows.add(soundRow(key, "none", "بدون صوت", null, cur == "none"))
        if (tts) rows.add(soundRow(key, "tts", "صوت ناطق (قراءة الذكر)", "يتطلب صوتًا عربيًا في الهاتف", cur == "tts"))
        if (random) rows.add(soundRow(key, "random", "عشوائي", "من أصوات هذا الذكر", cur == "random"))
        val built = Sounds.builtin(this).filter(filter)
        for (s in built) rows.add(soundRow(key, s.id, s.label, null, cur == s.id))
        for (s in Sounds.customList(this)) rows.add(soundRow(key, s.id, s.label, "ملف مضاف", cur == s.id))
        c.addView(group(*rows.toTypedArray()))
        if (built.isEmpty()) {
            c.addView(
                tv(
                    "لا توجد أصوات مدمجة هنا. ارفع ملفات الصوت إلى مجلد sounds في GitHub " +
                        "ثم أعد بناء التطبيق، أو أضف صوتًا من هاتفك.",
                    13f, Night.MUTED
                ), lp(MATCH, WRAP, top = 10)
            )
        }
        c.addView(
            group(
                settingRow("upload_file", "إضافة صوت من هاتفك", "mp3 أو m4a أو ogg") {
                    customPicker.launch(arrayOf("audio/*"))
                }
            ),
            lp(MATCH, WRAP, top = 16)
        )
        return c
    }

    private fun soundRow(key: String, id: String, label: String, sub: String?, selected: Boolean): LinearLayout {
        val row = hbox().apply { setPadding(dp(16), dp(12), dp(8), dp(12)) }
        row.addView(
            iconView(
                if (selected) "radio_button_checked" else "radio_button_unchecked", 22f,
                if (selected) Night.GOLD else Night.MUTED
            ),
            LinearLayout.LayoutParams(dp(28), WRAP)
        )
        val col = vbox()
        col.addView(tv(label, 16f, Night.TEXT))
        if (sub != null) col.addView(tv(sub, 12f, Night.MUTED))
        row.addView(col, lp(0, WRAP, 1f, start = 14))
        val canPreview = id != "none" && id != "tts" && id != "random"
        if (canPreview) {
            val pv = iconView(if (previewId == id) "stop" else "play_arrow", 24f, Night.TEAL).apply {
                setPadding(dp(12), dp(6), dp(12), dp(6))
                setOnClickListener { togglePreview(id) }
            }
            previewIcons[id] = pv
            row.addView(pv)
        }
        row.setOnClickListener {
            prefs().edit().putString(key, id).apply()
            stopPreview()
            showSub()
        }
        return row
    }

    private fun refreshPreviewIcons() {
        for ((k, v) in previewIcons) {
            v.setIcon(if (k == previewId) "stop" else "play_arrow")
        }
    }

    private fun togglePreview(id: String) {
        if (previewId == id) {
            stopPreview()
            return
        }
        stopPreview()
        val mp = Sounds.createPlayer(
            this, id, AudioAttributes.USAGE_MEDIA, AudioAttributes.CONTENT_TYPE_MUSIC
        )
        if (mp == null) {
            toast("تعذر تشغيل الملف")
            return
        }
        preview = mp
        previewId = id
        try {
            mp.setOnPreparedListener { it.start() }
            mp.setOnCompletionListener { handler.post { stopPreview() } }
            mp.setOnErrorListener { _, _, _ ->
                handler.post { stopPreview() }
                true
            }
            mp.prepareAsync()
        } catch (e: Exception) {
            stopPreview()
        }
        refreshPreviewIcons()
    }

    private fun stopPreview() {
        try {
            preview?.release()
        } catch (e: Exception) {
            // ignore
        }
        preview = null
        previewId = null
        refreshPreviewIcons()
    }

    // ------------------------------------------------------------ azkar tab

    private fun intervalLabel(min: Int): String = when {
        min == 60 -> "كل ساعة"
        min == 120 -> "كل ساعتين"
        min <= 10 -> arNum(this, "كل " + min + " دقائق")
        else -> arNum(this, "كل " + min + " دقيقة")
    }

    private fun selSet(): MutableSet<Int> =
        (prefs().getString("dhikr_sel", "0,1,2") ?: "0")
            .split(",").mapNotNull { it.trim().toIntOrNull() }.toMutableSet()

    private fun saveSel(s: Set<Int>) {
        prefs().edit().putString("dhikr_sel", s.sorted().joinToString(",")).apply()
    }

    private fun hourLabel(h: Int): String = arNum(this, String.format(Locale.US, "%02d:00", h))

    private fun hourDialog(title: String, key: String, def: Int) {
        val names = Array(24) { hourLabel(it) }
        choose(title, names, prefs().getInt(key, def)) { i ->
            prefs().edit().putInt(key, i).apply()
            Scheduler.scheduleDhikr(this)
            showTab(1)
        }
    }

    private fun buildAzkar(): LinearLayout {
        val p = prefs()
        val c = pageBox()
        c.addView(pageTitle("الأذكار"))

        c.addView(sectionTitle("التذكير الدوري"))
        val mins = intArrayOf(5, 10, 15, 30, 60, 120)
        val labels = mins.map { intervalLabel(it) }
        val quietOn = p.getBoolean("quiet_on", false)
        c.addView(
            group(
                switchRow(
                    "alarm", "تشغيل التذكير الدوري", "إشعار وصوت بالأذكار المختارة",
                    p.getBoolean("dhikr_on", false)
                ) { v ->
                    p.edit().putBoolean("dhikr_on", v).apply()
                    if (v) Scheduler.scheduleDhikr(this) else Scheduler.cancelDhikr(this)
                },
                chipsRow(labels, mins.indexOf(p.getInt("dhikr_min", 30)).coerceAtLeast(0)) { i ->
                    p.edit().putInt("dhikr_min", mins[i]).apply()
                    Scheduler.scheduleDhikr(this)
                },
                switchRow("bedtime", "ساعات الهدوء", "بدون أذكار في هذه الفترة", quietOn) { v ->
                    p.edit().putBoolean("quiet_on", v).apply()
                    Scheduler.scheduleDhikr(this)
                    showTab(1)
                },
                settingRow("schedule", "بداية الهدوء", hourLabel(p.getInt("quiet_start", 23))) {
                    hourDialog("بداية الهدوء", "quiet_start", 23)
                },
                settingRow("schedule", "نهاية الهدوء", hourLabel(p.getInt("quiet_end", 5))) {
                    hourDialog("نهاية الهدوء", "quiet_end", 5)
                }
            )
        )

        c.addView(sectionTitle("الأذكار المختارة وأصواتها"))
        val sel = selSet()
        val rows = ArrayList<View>()
        for (i in PrayerData.DHIKR.indices) rows.add(dhikrRow(i, sel))
        c.addView(group(*rows.toTypedArray()))
        c.addView(
            group(settingRow("play_arrow", "تجربة التذكير الآن", null) {
                ContextCompat.startForegroundService(this, Intent(this, DhikrService::class.java))
            }),
            lp(MATCH, WRAP, top = 12)
        )

        c.addView(sectionTitle("السبحة"))
        c.addView(buildTasbeeh())
        return c
    }

    private fun dhikrRow(i: Int, sel: MutableSet<Int>): LinearLayout {
        val row = hbox().apply { setPadding(dp(16), dp(12), dp(8), dp(12)) }
        val check = iconView(
            if (sel.contains(i)) "check_box" else "check_box_outline_blank", 24f,
            if (sel.contains(i)) Night.GOLD else Night.MUTED
        )
        row.addView(check, LinearLayout.LayoutParams(dp(28), WRAP))
        val cur = prefs().getString("dhikr_sound_" + i, null) ?: "tts"
        val col = vbox()
        col.addView(tv(PrayerData.DHIKR[i], 16f, Night.TEXT))
        col.addView(tv(Sounds.labelOf(this, cur), 12f, Night.MUTED))
        row.addView(col, lp(0, WRAP, 1f, start = 14))
        val music = iconView("music_note", 22f, Night.TEAL).apply {
            setPadding(dp(14), dp(8), dp(14), dp(8))
            setOnClickListener {
                val key = PrayerData.DHIKR_KEYS[i]
                openSub("صوت: " + PrayerData.DHIKR[i]) {
                    soundPicker(
                        "dhikr_sound_" + i,
                        { s -> s.name.startsWith("dhikr_" + key + "_") || s.category == "tone" },
                        tts = true, none = true, random = true, fallback = "tts"
                    )
                }
            }
        }
        row.addView(music)
        row.setOnClickListener {
            if (sel.contains(i)) {
                if (sel.size <= 1) {
                    toast("اختر ذكرًا واحدًا على الأقل")
                    return@setOnClickListener
                }
                sel.remove(i)
            } else {
                sel.add(i)
            }
            saveSel(sel)
            check.setIcon(if (sel.contains(i)) "check_box" else "check_box_outline_blank")
            check.setTextColor(if (sel.contains(i)) Night.GOLD else Night.MUTED)
        }
        return row
    }

    private fun buildTasbeeh(): LinearLayout {
        val p = prefs()
        val card = vbox().apply {
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(16), dp(18), dp(16), dp(18))
            background = roundBg(Night.CARD, 20)
        }
        val phrase = tv(
            PrayerData.DHIKR[p.getInt("tasbeeh_idx", 1).coerceIn(0, PrayerData.DHIKR.size - 1)],
            20f, Night.TEXT, true
        ).apply { gravity = Gravity.CENTER }
        phrase.setOnClickListener {
            choose(
                "اختر الذكر", PrayerData.DHIKR,
                p.getInt("tasbeeh_idx", 1).coerceIn(0, PrayerData.DHIKR.size - 1)
            ) { i ->
                p.edit().putInt("tasbeeh_idx", i).putInt("tasbeeh_count", 0).apply()
                showTab(1)
            }
        }
        card.addView(phrase, lp(MATCH, WRAP, bottom = 4))
        card.addView(tv("اضغط على الاسم لتغيير الذكر", 12f, Night.MUTED))

        var target = p.getInt("tasbeeh_target", 33)
        val count0 = p.getInt("tasbeeh_count", 0)
        val countView = tv(arNum(this, count0.toString()), 56f, Night.GOLD, true).apply {
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(Night.CARD2)
                setStroke(dp(3), Night.GOLD)
            }
        }
        val bar = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = if (target > 0) target else 100
            progress = if (target > 0) count0 else count0 % 100
            progressTintList = ColorStateList.valueOf(Night.GOLD)
            progressBackgroundTintList = ColorStateList.valueOf(Night.CARD2)
        }
        countView.setOnClickListener { v ->
            var n = p.getInt("tasbeeh_count", 0) + 1
            if (target > 0 && n > target) n = 1
            p.edit().putInt("tasbeeh_count", n).apply()
            countView.text = arNum(this, n.toString())
            bar.max = if (target > 0) target else 100
            bar.progress = if (target > 0) n else n % 100
            if (target > 0 && n == target) {
                v.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS)
                toast("تم الورد")
            } else {
                v.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
            }
        }
        card.addView(countView, lp(dp(180), dp(180), top = 16, bottom = 16))
        card.addView(bar, lp(MATCH, dp(8)))

        val targets = intArrayOf(33, 99, 100, 0)
        val tLabels = listOf(arNum(this, "33"), arNum(this, "99"), arNum(this, "100"), "مفتوح")
        card.addView(
            chipsRow(tLabels, targets.indexOf(target).coerceAtLeast(0)) { i ->
                target = targets[i]
                p.edit().putInt("tasbeeh_target", target).putInt("tasbeeh_count", 0).apply()
                countView.text = arNum(this, "0")
                bar.max = if (target > 0) target else 100
                bar.progress = 0
            }
        )
        val reset = tv("إعادة العدّاد", 14f, Night.onGold, true).apply {
            gravity = Gravity.CENTER
            setPadding(dp(24), dp(10), dp(24), dp(10))
            background = roundBg(Night.GOLD, 20)
            setOnClickListener {
                p.edit().putInt("tasbeeh_count", 0).apply()
                countView.text = arNum(this@MainActivity, "0")
                bar.progress = 0
            }
        }
        card.addView(reset, lp(WRAP, WRAP, top = 4))
        return card
    }

    // ------------------------------------------------------------ qibla tab

    private fun qiblaBearingFor(lat: Double, lon: Double): Double {
        val k1 = Math.toRadians(21.4225)
        val k2 = Math.toRadians(39.8262)
        val p1 = Math.toRadians(lat)
        val dl = k2 - Math.toRadians(lon)
        val y = Math.sin(dl) * Math.cos(k1)
        val x = Math.cos(p1) * Math.sin(k1) - Math.sin(p1) * Math.cos(k1) * Math.cos(dl)
        return (Math.toDegrees(Math.atan2(y, x)) + 360.0) % 360.0
    }

    private fun buildQibla(): LinearLayout {
        val c = pageBox()
        c.addView(pageTitle("اتجاه القبلة"))
        val cv = CompassView(this)
        compass = cv
        val co = PrayerData.coords(this)
        if (co != null) {
            qiblaBearing = qiblaBearingFor(co.first, co.second)
            cv.qibla = qiblaBearing.toFloat()
            cv.hasQibla = true
        } else {
            qiblaBearing = Double.NaN
            cv.hasQibla = false
        }
        c.addView(cv, lp(MATCH, dp(340), top = 6))
        val info = tv(
            if (co == null) "حدّد موقعك أولًا لحساب اتجاه القبلة"
            else "اتجاه القبلة: " + arNum(this, qiblaBearing.toInt().toString()) + " درجة من الشمال",
            17f, Night.TEXT, true
        ).apply { gravity = Gravity.CENTER }
        qiblaInfo = info
        c.addView(info, lp(MATCH, WRAP, top = 12))
        val hasSensor = (getSystemService(SENSOR_SERVICE) as SensorManager)
            .getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR) != null
        val hint = tv(
            if (hasSensor) "ضع الهاتف أفقيًا بعيدًا عن المعادن والمغناطيس، وحرّكه على شكل رقم 8 لمعايرة البوصلة. عندما يتوهج الإطار الذهبي تكون متجهًا إلى القبلة."
            else "جهازك لا يحتوي على مستشعر للبوصلة، استخدم الزاوية المذكورة أعلاه مع بوصلة خارجية.",
            13f, Night.MUTED
        ).apply { gravity = Gravity.CENTER }
        c.addView(hint, lp(MATCH, WRAP, top = 10))
        return c
    }

    private fun updateSensor() {
        if (tab == 2 && stack.isEmpty() && compass != null) startSensor() else stopSensor()
    }

    private fun startSensor() {
        if (sensorOn) return
        val sm = getSystemService(SENSOR_SERVICE) as SensorManager
        val s = sm.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR) ?: return
        sm.registerListener(sensorListener, s, SensorManager.SENSOR_DELAY_UI)
        sensorOn = true
    }

    private fun stopSensor() {
        if (!sensorOn) return
        try {
            (getSystemService(SENSOR_SERVICE) as SensorManager).unregisterListener(sensorListener)
        } catch (e: Exception) {
            // ignore
        }
        sensorOn = false
    }
}
'''

parts = re.split(r'^=== (.+?) ===\n', BUNDLE, flags=re.M)
count = 0
for i in range(1, len(parts), 2):
    path = parts[i].strip()
    content = parts[i + 1]
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
print("Generated source files:", count)

# ---- copy sounds (any file inside the repo-level "sounds" folder) ----
assets = "app/src/main/assets"
os.makedirs(assets, exist_ok=True)
if os.path.isdir("sounds"):
    dst = os.path.join(assets, "sounds")
    os.makedirs(dst, exist_ok=True)
    total = 0
    for name in sorted(os.listdir("sounds")):
        src = os.path.join("sounds", name)
        if os.path.isfile(src) and name.lower() != "readme.txt":
            shutil.copy(src, os.path.join(dst, name))
            total += os.path.getsize(src)
            print("sound:", name)
    print("Sounds size (MB): %.1f" % (total / 1048576.0))
else:
    print("NOTE: no 'sounds' folder found; the app will use system sounds.")

# ---- copy the icon font (any .otf/.ttf in the repo root) ----
fonts = [f for f in os.listdir(".") if f.lower().endswith((".otf", ".ttf"))]
if fonts:
    fonts.sort(key=lambda n: (0 if "round" in n.lower() else 1, n))
    shutil.copy(fonts[0], os.path.join(assets, "icons.otf"))
    print("icon font:", fonts[0])
else:
    print("WARNING: icon font not found in repo root. Upload MaterialIconsRound-Regular.otf")
