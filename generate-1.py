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
        versionCode = 1
        versionName = "1.0"
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
            android:exported="true">
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
            android:name=".AdhanReceiver"
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
        <item name="android:navigationBarColor">#0A0E1A</item>
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
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import java.util.Calendar
import java.util.Locale

object Night {
    val BG = Color.parseColor("#0A0E1A")
    val CARD = Color.parseColor("#131A2E")
    val CARD2 = Color.parseColor("#1D2742")
    val GOLD = Color.parseColor("#F2C46D")
    val TEAL = Color.parseColor("#4DD0B5")
    val TEXT = Color.parseColor("#EAEDF7")
    val MUTED = Color.parseColor("#8B93B0")
}

fun Context.prefs(): SharedPreferences =
    getSharedPreferences("adhan", Context.MODE_PRIVATE)

fun Context.dp(v: Int): Int =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()

fun Context.roundBg(color: Int, radiusDp: Int): GradientDrawable =
    GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(radiusDp).toFloat()
    }

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
    val ICONS = arrayOf("🌙", "🌅", "☀️", "🌤️", "🌇", "🌌")

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

    fun hasLocation(c: Context): Boolean {
        val p = c.prefs()
        return if (p.getString("mode", "gps") == "city") {
            !p.getString("city", "").isNullOrEmpty()
        } else {
            p.contains("lat") && p.contains("lon")
        }
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
            if (root.optInt("code") != 200) null else root.getJSONArray("data").toString()
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
                times[i] = c2.timeInMillis
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
    const val ACTION_ADHAN = "com.nightadhan.app.ADHAN"
    const val ACTION_DHIKR = "com.nightadhan.app.DHIKR"

    private fun am(c: Context) = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
    private fun adhanIntent(c: Context) = Intent(c, AdhanReceiver::class.java).setAction(ACTION_ADHAN)
    private fun dhikrIntent(c: Context) = Intent(c, DhikrReceiver::class.java).setAction(ACTION_DHIKR)

    @Synchronized
    fun scheduleAdhans(c: Context) {
        val alarm = am(c)
        val p = c.prefs()
        for (k in 0 until 30) {
            val old = PendingIntent.getBroadcast(
                c, 200 + k, adhanIntent(c),
                PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
            )
            if (old != null) {
                alarm.cancel(old)
                old.cancel()
            }
        }
        val now = System.currentTimeMillis()
        val list = ArrayList<Pair<Long, Int>>()
        for (d in 0..2) {
            val cl = Calendar.getInstance()
            cl.add(Calendar.DAY_OF_MONTH, d)
            val dd = PrayerData.dayData(c, cl) ?: continue
            for (i in intArrayOf(0, 2, 3, 4, 5)) {
                if (p.getBoolean("adhan_" + i, true) && dd.times[i] > now) {
                    list.add(Pair(dd.times[i], i))
                }
            }
        }
        list.sortBy { it.first }
        val show = PendingIntent.getActivity(
            c, 0, Intent(c, MainActivity::class.java), PendingIntent.FLAG_IMMUTABLE
        )
        for ((k, item) in list.take(10).withIndex()) {
            val pi = PendingIntent.getBroadcast(
                c, 200 + k, adhanIntent(c).putExtra("prayer", item.second),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            try {
                alarm.setAlarmClock(AlarmManager.AlarmClockInfo(item.first, show), pi)
            } catch (e: Exception) {
                // ignore
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
        val alarm = am(c)
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

    fun pickDhikr(c: Context): String {
        val sel = (c.prefs().getString("dhikr_sel", "0,1,2") ?: "0")
            .split(",")
            .mapNotNull { it.trim().toIntOrNull() }
            .filter { it in PrayerData.DHIKR.indices }
        val list = if (sel.isEmpty()) listOf(0) else sel
        return PrayerData.DHIKR[list.random()]
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
    const val CH_ADHAN = "adhan_v1"
    const val CH_DHIKR = "dhikr_v1"

    fun ensure(c: Context) {
        val nm = c.getSystemService(NotificationManager::class.java)
        val a = NotificationChannel(CH_ADHAN, "الأذان", NotificationManager.IMPORTANCE_HIGH).apply {
            description = "إشعار وقت الأذان"
            setSound(null, null)
            enableVibration(true)
            lockscreenVisibility = Notification.VISIBILITY_PUBLIC
        }
        val d = NotificationChannel(CH_DHIKR, "الأذكار الدورية", NotificationManager.IMPORTANCE_DEFAULT).apply {
            description = "تذكير دوري بالأذكار"
            setSound(null, null)
            enableVibration(false)
        }
        nm.createNotificationChannel(a)
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
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import java.io.File
import java.util.Locale

class AdhanService : Service() {

    companion object {
        const val ACTION_STOP = "com.nightadhan.app.STOP_ADHAN"
        const val ID = 2001

        @Volatile
        var playing = false
    }

    private var mp: MediaPlayer? = null
    private var prayer = 2
    private var started = false
    private var finished = false
    private val handler = Handler(Looper.getMainLooper())

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            if (started) finishAdhan() else stopSelf()
            return START_NOT_STICKY
        }
        prayer = intent?.getIntExtra("prayer", 2) ?: 2
        started = true
        finished = false
        playing = true
        Notif.ensure(this)
        ServiceCompat.startForeground(
            this, ID, buildNotif(true), ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
        )
        Thread {
            PrayerData.ensureData(this)
            Scheduler.scheduleAdhans(this)
        }.start()
        startAudio()
        handler.removeCallbacksAndMessages(null)
        handler.postDelayed({ finishAdhan() }, 6 * 60 * 1000L)
        return START_NOT_STICKY
    }

    private fun buildNotif(ongoing: Boolean): Notification {
        val name = PrayerData.NAMES[prayer]
        val text = if (prayer == 0) "الصلاة خير من النوم · قُم إلى صلاة الفجر"
        else "حان وقت صلاة " + name + " · قُم إلى الصلاة"
        val b = NotificationCompat.Builder(this, Notif.CH_ADHAN)
            .setSmallIcon(R.drawable.ic_stat)
            .setContentTitle("حان الآن موعد أذان " + name)
            .setContentText(text)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setContentIntent(Notif.openApp(this))
            .setOngoing(ongoing)
            .setAutoCancel(!ongoing)
        if (ongoing) {
            val stop = PendingIntent.getService(
                this, 2,
                Intent(this, AdhanService::class.java).setAction(ACTION_STOP),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
            )
            b.addAction(0, "⏹ إيقاف الأذان", stop)
        }
        return b.build()
    }

    private fun startAudio() {
        releasePlayer()
        val p = prefs()
        var path: String? = if (prayer == 0) p.getString("adhan_fajr_file", null) else null
        if (path == null || !File(path).exists()) path = p.getString("adhan_file", null)
        val player = MediaPlayer()
        mp = player
        try {
            player.setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            if (path != null && File(path).exists()) {
                player.setDataSource(path)
            } else {
                player.setDataSource(this, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
            }
            player.setWakeMode(this, PowerManager.PARTIAL_WAKE_LOCK)
            player.setOnPreparedListener { it.start() }
            player.setOnCompletionListener { finishAdhan() }
            player.setOnErrorListener { _, _, _ ->
                finishAdhan()
                true
            }
            player.prepareAsync()
        } catch (e: Exception) {
            finishAdhan()
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

    private fun finishAdhan() {
        if (finished) return
        finished = true
        playing = false
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        stopForeground(Service.STOP_FOREGROUND_DETACH)
        if (started) {
            val nm = getSystemService(NotificationManager::class.java)
            nm.notify(ID, buildNotif(false))
        }
        stopSelf()
    }

    override fun onDestroy() {
        playing = false
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        super.onDestroy()
    }
}

class DhikrService : Service() {

    companion object {
        const val ID = 2002
    }

    private var tts: TextToSpeech? = null
    private var mp: MediaPlayer? = null
    private var done = false
    private val handler = Handler(Looper.getMainLooper())

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        done = false
        Notif.ensure(this)
        val phrase = Scheduler.pickDhikr(this)
        val n = NotificationCompat.Builder(this, Notif.CH_DHIKR)
            .setSmallIcon(R.drawable.ic_stat)
            .setContentTitle("📿 تذكير")
            .setContentText(phrase)
            .setStyle(NotificationCompat.BigTextStyle().bigText(phrase))
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setContentIntent(Notif.openApp(this))
            .setAutoCancel(true)
            .setTimeoutAfter(10 * 60 * 1000L)
            .build()
        ServiceCompat.startForeground(
            this, ID, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
        )
        Scheduler.scheduleDhikr(this)
        handler.removeCallbacksAndMessages(null)
        handler.postDelayed({ finishUp() }, 60000L)
        if (AdhanService.playing) {
            finishUp()
        } else {
            play(phrase)
        }
        return START_NOT_STICKY
    }

    private fun play(phrase: String) {
        val p = prefs()
        val mode = p.getInt("dhikr_mode", 0)
        val file = p.getString("dhikr_file", null)
        if (mode == 1 && file != null && File(file).exists()) {
            playFile(file)
        } else if (mode == 0) {
            speak(phrase)
        } else {
            beep()
        }
    }

    private fun playFile(path: String) {
        try {
            val player = MediaPlayer()
            mp = player
            player.setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            player.setDataSource(path)
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

class AdhanReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val i = Intent(context, AdhanService::class.java)
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
                Scheduler.scheduleAdhans(app)
                Scheduler.scheduleDhikr(app)
            } finally {
                pending.finish()
            }
            PrayerData.ensureData(app)
            Scheduler.scheduleAdhans(app)
        }.start()
    }
}
=== app/src/main/java/com/nightadhan/app/MainActivity.kt ===
package com.nightadhan.app

import android.Manifest
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.ColorStateList
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.location.Geocoder
import android.location.Location
import android.location.LocationManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.core.location.LocationManagerCompat
import java.io.File
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

class MainActivity : ComponentActivity() {

    private lateinit var placeText: TextView
    private lateinit var dateText: TextView
    private lateinit var hijriText: TextView
    private lateinit var nextLabel: TextView
    private lateinit var nextName: TextView
    private lateinit var nextTime: TextView
    private lateinit var countdown: TextView
    private lateinit var progress: ProgressBar
    private lateinit var rowsBox: LinearLayout
    private lateinit var statusText: TextView
    private lateinit var dhikrStatus: TextView

    private val handler = Handler(Looper.getMainLooper())
    private var nextIdx = 2
    private var nextAt = 0L
    private var prevAt = 0L
    private var pendingPick = "adhan"

    private val tick = object : Runnable {
        override fun run() {
            updateCountdown()
            handler.postDelayed(this, 1000)
        }
    }

    private val notifLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    private val locPermLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { res ->
            if (res.values.any { it }) useGps() else toast("بدون إذن الموقع اختر المدينة يدويًا")
        }

    private val picker =
        registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
            if (uri != null) {
                val target = pendingPick
                Thread {
                    try {
                        val f = File(filesDir, target + ".bin")
                        contentResolver.openInputStream(uri)?.use { input ->
                            f.outputStream().use { out -> input.copyTo(out) }
                        }
                        prefs().edit().putString(target + "_file", f.absolutePath).apply()
                        runOnUiThread { toast("تم حفظ الصوت ✅") }
                    } catch (e: Exception) {
                        runOnUiThread { toast("تعذر قراءة الملف") }
                    }
                }.start()
            }
        }

    private fun toast(m: String) = Toast.makeText(this, m, Toast.LENGTH_LONG).show()

    // ------------------------------------------------------------ UI

    private fun tv(text: String, size: Float, color: Int, bold: Boolean = false): TextView =
        TextView(this).apply {
            this.text = text
            textSize = size
            setTextColor(color)
            if (bold) setTypeface(typeface, Typeface.BOLD)
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Notif.ensure(this)

        val scroll = ScrollView(this).apply {
            setBackgroundColor(Night.BG)
            layoutDirection = View.LAYOUT_DIRECTION_RTL
        }
        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), dp(18), dp(16), dp(28))
        }
        scroll.addView(content)

        // top bar
        val top = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        top.addView(
            tv("✦ مؤذن", 24f, Night.GOLD, true),
            LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        )
        val gear = tv("⚙", 26f, Night.TEXT)
        gear.setPadding(dp(12), dp(4), dp(12), dp(4))
        gear.setOnClickListener { settingsMenu() }
        top.addView(gear)
        content.addView(top)

        placeText = tv("", 14f, Night.MUTED)
        placeText.setPadding(0, dp(6), 0, 0)
        content.addView(placeText)
        dateText = tv("", 15f, Night.TEXT)
        content.addView(dateText)
        hijriText = tv("", 15f, Night.TEAL)
        hijriText.setPadding(0, 0, 0, dp(14))
        content.addView(hijriText)

        // next prayer card
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(20), dp(22), dp(20), dp(22))
            background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(0xFF2A3F73.toInt(), 0xFF131A2E.toInt())
            ).apply { cornerRadius = dp(24).toFloat() }
        }
        nextLabel = tv("", 14f, Night.GOLD)
        nextName = tv("", 34f, Night.TEXT, true)
        nextTime = tv("", 18f, Night.MUTED)
        countdown = tv("", 42f, Night.GOLD, true)
        countdown.typeface = Typeface.MONOSPACE
        countdown.setPadding(0, dp(10), 0, dp(10))
        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 1000
            progressTintList = ColorStateList.valueOf(Night.GOLD)
            progressBackgroundTintList = ColorStateList.valueOf(Night.CARD2)
        }
        card.addView(nextLabel)
        card.addView(nextName)
        card.addView(nextTime)
        card.addView(countdown)
        card.addView(
            progress,
            LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(8))
        )
        content.addView(card)

        // prayer rows
        rowsBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(6), dp(6), dp(6), dp(6))
            background = roundBg(Night.CARD, 20)
        }
        val rp = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        rp.topMargin = dp(16)
        content.addView(rowsBox, rp)

        // buttons
        val btns = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
        }
        val b1 = button("📍 تحديث الموقع") { locationChoice() }
        val b2 = button("🔄 تحديث المواقيت") { forceReload() }
        val bp1 = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
        bp1.marginEnd = dp(8)
        btns.addView(b1, bp1)
        btns.addView(b2, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        val bl = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        bl.topMargin = dp(16)
        content.addView(btns, bl)

        // dhikr status
        dhikrStatus = tv("", 15f, Night.TEXT)
        dhikrStatus.setPadding(dp(16), dp(16), dp(16), dp(16))
        dhikrStatus.background = roundBg(Night.CARD, 16)
        dhikrStatus.setOnClickListener { dhikrMenu() }
        val dl = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        dl.topMargin = dp(12)
        content.addView(dhikrStatus, dl)

        statusText = tv("", 13f, Night.MUTED)
        statusText.gravity = Gravity.CENTER
        statusText.setPadding(0, dp(12), 0, 0)
        content.addView(statusText)

        setContentView(scroll)

        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED
        ) {
            notifLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
        if (!PrayerData.hasLocation(this)) locationChoice()
    }

    private fun button(label: String, onClick: () -> Unit): TextView =
        tv(label, 14f, Night.TEXT, true).apply {
            gravity = Gravity.CENTER
            setPadding(dp(8), dp(14), dp(8), dp(14))
            background = roundBg(Night.CARD2, 14)
            setOnClickListener { onClick() }
        }

    override fun onResume() {
        super.onResume()
        render()
        updateDhikrStatus()
        handler.removeCallbacks(tick)
        handler.post(tick)
        if (PrayerData.hasLocation(this)) reload()
    }

    override fun onPause() {
        super.onPause()
        handler.removeCallbacks(tick)
    }

    // ------------------------------------------------------------ rendering

    private fun render() {
        val p = prefs()
        var place = p.getString("place", "") ?: ""
        if (place.isEmpty() && p.contains("lat")) {
            place = p.getString("lat", "") + ", " + p.getString("lon", "")
        }
        placeText.text = if (place.isEmpty()) "" else "📍 " + place
        val now = System.currentTimeMillis()
        val cal = Calendar.getInstance()
        val today = PrayerData.dayData(this, cal)
        dateText.text = arNum(this, SimpleDateFormat("EEEE، d MMMM yyyy", Locale("ar")).format(cal.time))
        rowsBox.removeAllViews()
        if (today == null) {
            hijriText.text = ""
            nextAt = 0L
            nextLabel.text = ""
            nextTime.text = ""
            countdown.text = ""
            progress.progress = 0
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
        nextName.text = PrayerData.ICONS[nextIdx] + "  " + PrayerData.NAMES[nextIdx]
        nextTime.text = clockText(this, nextAt)

        for (i in 0 until 6) {
            val isNext = i == nextIdx
            val passed = today.times[i] <= now && !isNext
            val row = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                setPadding(dp(14), dp(14), dp(14), dp(14))
                if (isNext) background = roundBg(Night.CARD2, 14)
            }
            val col = if (passed) Night.MUTED else Night.TEXT
            row.addView(tv(PrayerData.ICONS[i], 20f, col))
            val name = tv(PrayerData.NAMES[i], 18f, if (isNext) Night.GOLD else col, isNext)
            name.setPadding(dp(12), 0, 0, 0)
            row.addView(name, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
            row.addView(tv(clockText(this, today.times[i]), 18f, if (isNext) Night.GOLD else col, isNext))
            if (i != 1) {
                val on = prefs().getBoolean("adhan_" + i, true)
                val bell = tv(if (on) "🔔" else "🔕", 20f, Night.TEXT)
                bell.setPadding(dp(14), 0, 0, 0)
                bell.setOnClickListener {
                    val now2 = !prefs().getBoolean("adhan_" + i, true)
                    prefs().edit().putBoolean("adhan_" + i, now2).apply()
                    Thread { Scheduler.scheduleAdhans(this) }.start()
                    toast(if (now2) "تم تفعيل أذان " + PrayerData.NAMES[i] else "تم إيقاف أذان " + PrayerData.NAMES[i])
                    render()
                }
                row.addView(bell)
            } else {
                val sp = tv("  ", 20f, Night.TEXT)
                sp.setPadding(dp(14), 0, 0, 0)
                row.addView(sp)
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

    private fun updateDhikrStatus() {
        val p = prefs()
        dhikrStatus.text = if (p.getBoolean("dhikr_on", false))
            "📿 التذكير بالأذكار: " + intervalText(p.getInt("dhikr_min", 30)) + "  (اضغط للتعديل)"
        else
            "📿 التذكير بالأذكار متوقف — اضغط للتفعيل"
    }

    private fun intervalText(min: Int): String = when {
        min == 60 -> "كل ساعة"
        min == 120 -> "كل ساعتين"
        min <= 10 -> arNum(this, "كل " + min + " دقائق")
        else -> arNum(this, "كل " + min + " دقيقة")
    }

    // ------------------------------------------------------------ data loading

    private fun reload() {
        statusText.text = "جاري تحديث المواقيت..."
        Thread {
            val ok = PrayerData.ensureData(this)
            Scheduler.scheduleAdhans(this)
            runOnUiThread {
                statusText.text = if (ok) "" else "تعذر جلب المواقيت، تأكد من الإنترنت"
                render()
            }
        }.start()
    }

    private fun forceReload() {
        PrayerData.clearCache(this)
        prefs().edit().remove("cache_key").apply()
        reload()
    }

    // ------------------------------------------------------------ location

    private fun locationChoice() {
        val items = arrayOf("📡 تحديد موقعي تلقائيًا (GPS)", "🏙 إدخال المدينة يدويًا")
        AlertDialog.Builder(this)
            .setTitle("تحديد الموقع")
            .setItems(items) { _, i ->
                if (i == 0) useGps() else cityDialog()
            }.show()
    }

    private fun cityDialog() {
        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(10), dp(20), 0)
        }
        val city = EditText(this).apply { hint = "المدينة بالإنجليزية (مثال: Cairo)"; setSingleLine() }
        val country = EditText(this).apply { hint = "الدولة بالإنجليزية (مثال: Egypt)"; setSingleLine() }
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
                lm, provider, null, ContextCompat.getMainExecutor(this),
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
            runOnUiThread { reload() }
        }.start()
    }

    // ------------------------------------------------------------ settings

    private fun settingsMenu() {
        val items = arrayOf(
            "📍 تغيير الموقع",
            "🧮 طريقة حساب المواقيت",
            "🕌 حساب العصر (الجمهور / الحنفي)",
            "🔊 اختيار صوت الأذان",
            "🌙 اختيار أذان الفجر (اختياري)",
            "▶ تجربة الأذان الآن",
            "📿 إعدادات الأذكار الدورية",
            "🔋 ضمان عمل التنبيهات (البطارية)",
            "🔢 الأرقام: عربية / إنجليزية"
        )
        AlertDialog.Builder(this)
            .setItems(items) { _, i ->
                when (i) {
                    0 -> locationChoice()
                    1 -> methodDialog()
                    2 -> schoolDialog()
                    3 -> pickFile("adhan")
                    4 -> pickFile("adhan_fajr")
                    5 -> ContextCompat.startForegroundService(
                        this, Intent(this, AdhanService::class.java).putExtra("prayer", 2)
                    )
                    6 -> dhikrMenu()
                    7 -> batteryHelp()
                    else -> {
                        val cur = prefs().getBoolean("ar_digits", true)
                        prefs().edit().putBoolean("ar_digits", !cur).apply()
                        render()
                        updateDhikrStatus()
                    }
                }
            }.show()
    }

    private fun pickFile(target: String) {
        pendingPick = target
        toast(
            if (target == "dhikr") "اختر ملفًا صوتيًا للذكر"
            else "اختر ملف الأذان من هاتفك (mp3 أو غيره)"
        )
        picker.launch(arrayOf("audio/*"))
    }

    private fun methodDialog() {
        val cur = prefs().getInt("method", 5)
        val idx = PrayerData.METHOD_IDS.indexOf(cur).coerceAtLeast(0)
        AlertDialog.Builder(this)
            .setTitle("طريقة الحساب")
            .setSingleChoiceItems(PrayerData.METHOD_NAMES, idx) { d, i ->
                prefs().edit().putInt("method", PrayerData.METHOD_IDS[i]).apply()
                d.dismiss()
                reload()
            }.show()
    }

    private fun schoolDialog() {
        val names = arrayOf("الجمهور (شافعي / مالكي / حنبلي)", "حنفي")
        AlertDialog.Builder(this)
            .setTitle("حساب وقت العصر")
            .setSingleChoiceItems(names, prefs().getInt("school", 0)) { d, i ->
                prefs().edit().putInt("school", i).apply()
                d.dismiss()
                reload()
            }.show()
    }

    private fun batteryHelp() {
        AlertDialog.Builder(this)
            .setTitle("ضمان عمل الأذان")
            .setMessage(
                "حتى يعمل الأذان والتذكير والهاتف مغلق الشاشة:\n\n" +
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
                    toast("افتح الإعدادات ← التطبيقات ← مؤذن")
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

    // ------------------------------------------------------------ dhikr

    private fun dhikrMenu() {
        val p = prefs()
        val on = p.getBoolean("dhikr_on", false)
        val modes = arrayOf("صوت ناطق (قراءة الذكر)", "ملف صوتي مخصص", "نغمة تنبيه فقط")
        val items = arrayOf(
            if (on) "⏸ إيقاف التذكير الدوري" else "▶ تشغيل التذكير الدوري",
            "⏱ المدة: " + intervalText(p.getInt("dhikr_min", 30)),
            "📿 اختيار الأذكار",
            "🔈 نوع الصوت: " + modes[p.getInt("dhikr_mode", 0).coerceIn(0, 2)],
            "🎵 اختيار ملف صوتي مخصص",
            "😴 ساعات الهدوء: " + quietText(),
            "▶ تجربة الآن"
        )
        AlertDialog.Builder(this)
            .setTitle("الأذكار الدورية")
            .setItems(items) { _, i ->
                when (i) {
                    0 -> {
                        p.edit().putBoolean("dhikr_on", !on).apply()
                        if (!on) Scheduler.scheduleDhikr(this) else Scheduler.cancelDhikr(this)
                        updateDhikrStatus()
                        toast(if (!on) "تم تشغيل التذكير" else "تم إيقاف التذكير")
                    }
                    1 -> intervalDialog()
                    2 -> dhikrChoiceDialog()
                    3 -> modeDialog(modes)
                    4 -> pickFile("dhikr")
                    5 -> quietMenu()
                    else -> ContextCompat.startForegroundService(
                        this, Intent(this, DhikrService::class.java)
                    )
                }
            }.show()
    }

    private fun intervalDialog() {
        val mins = intArrayOf(5, 10, 15, 30, 60, 120)
        val names = Array(mins.size) { intervalText(mins[it]) }
        val cur = mins.indexOf(prefs().getInt("dhikr_min", 30)).coerceAtLeast(0)
        AlertDialog.Builder(this)
            .setTitle("المدة بين التذكيرات")
            .setSingleChoiceItems(names, cur) { d, i ->
                prefs().edit().putInt("dhikr_min", mins[i]).apply()
                Scheduler.scheduleDhikr(this)
                updateDhikrStatus()
                d.dismiss()
            }.show()
    }

    private fun dhikrChoiceDialog() {
        val sel = (prefs().getString("dhikr_sel", "0,1,2") ?: "0")
            .split(",").mapNotNull { it.trim().toIntOrNull() }.toSet()
        val checked = BooleanArray(PrayerData.DHIKR.size) { sel.contains(it) }
        AlertDialog.Builder(this)
            .setTitle("اختر الأذكار")
            .setMultiChoiceItems(PrayerData.DHIKR, checked) { _, i, isChecked -> checked[i] = isChecked }
            .setPositiveButton("حفظ") { _, _ ->
                val s = checked.indices.filter { checked[it] }.joinToString(",")
                prefs().edit().putString("dhikr_sel", if (s.isEmpty()) "0" else s).apply()
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun modeDialog(modes: Array<String>) {
        AlertDialog.Builder(this)
            .setTitle("نوع الصوت")
            .setSingleChoiceItems(modes, prefs().getInt("dhikr_mode", 0).coerceIn(0, 2)) { d, i ->
                prefs().edit().putInt("dhikr_mode", i).apply()
                d.dismiss()
            }.show()
    }

    private fun hourLabel(h: Int): String = arNum(this, String.format(Locale.US, "%02d:00", h))

    private fun quietText(): String {
        val p = prefs()
        return if (p.getBoolean("quiet_on", false))
            hourLabel(p.getInt("quiet_start", 23)) + " ← " + hourLabel(p.getInt("quiet_end", 5))
        else "متوقفة"
    }

    private fun quietMenu() {
        val p = prefs()
        val on = p.getBoolean("quiet_on", false)
        val items = arrayOf(
            if (on) "إيقاف ساعات الهدوء" else "تشغيل ساعات الهدوء",
            "بداية الهدوء: " + hourLabel(p.getInt("quiet_start", 23)),
            "نهاية الهدوء: " + hourLabel(p.getInt("quiet_end", 5))
        )
        AlertDialog.Builder(this)
            .setTitle("ساعات الهدوء (بدون أذكار)")
            .setItems(items) { _, i ->
                when (i) {
                    0 -> {
                        p.edit().putBoolean("quiet_on", !on).apply()
                        Scheduler.scheduleDhikr(this)
                    }
                    1 -> hourDialog("بداية الهدوء", "quiet_start", 23)
                    else -> hourDialog("نهاية الهدوء", "quiet_end", 5)
                }
            }.show()
    }

    private fun hourDialog(title: String, key: String, def: Int) {
        val names = Array(24) { hourLabel(it) }
        AlertDialog.Builder(this)
            .setTitle(title)
            .setSingleChoiceItems(names, prefs().getInt(key, def)) { d, i ->
                prefs().edit().putInt(key, i).apply()
                Scheduler.scheduleDhikr(this)
                d.dismiss()
            }.show()
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
    print("created:", path)
print("Total files:", count)
