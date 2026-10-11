package ru.mihealthresearch.runtime.ru;

import android.net.Uri;
import android.text.TextUtils;
import android.webkit.WebView;
import android.widget.TextView;
import de.robv.android.xposed.IXposedHookInitPackageResources;
import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_InitPackageResources;
import de.robv.android.xposed.callbacks.XC_LoadPackage;
import java.util.LinkedHashMap;
import java.util.Map;

public final class RussianModule implements IXposedHookInitPackageResources, IXposedHookLoadPackage {
    private static final String TARGET_PACKAGE = "com.mi.healthresearch";
    private static final Map<String, String> RESOURCE_TRANSLATIONS = new LinkedHashMap<>();
    private static final Map<String, String> DYNAMIC_TEXT_TRANSLATIONS = new LinkedHashMap<>();

    static {
        RESOURCE_TRANSLATIONS.put("app_name", "Исследование здоровья Xiaomi");
        RESOURCE_TRANSLATIONS.put("health_title", "Исследование здоровья Xiaomi");
        RESOURCE_TRANSLATIONS.put("health_sub_title", "Здоровье в гармонии с жизнью");
        RESOURCE_TRANSLATIONS.put("health_tab_name", "Здоровье");
        RESOURCE_TRANSLATIONS.put("device_tab_name", "Устройства");
        RESOURCE_TRANSLATIONS.put("mine_tab_name", "Профиль");
        RESOURCE_TRANSLATIONS.put("health_heart_research", "Исследование здоровья сердца");
        RESOURCE_TRANSLATIONS.put("health_heart_research_title", "Исследование здоровья сердца");
        RESOURCE_TRANSLATIONS.put("health_blood_pressure_research_title", "Исследование артериального давления");
        RESOURCE_TRANSLATIONS.put("health_sleep_research_title", "Исследование апноэ сна");
        RESOURCE_TRANSLATIONS.put("health_sport_wounded_title", "Оценка риска беговых травм");
        RESOURCE_TRANSLATIONS.put("health_sport_wounded_title_desc", "Оценка риска беговых травм с учётом привычек бега, перенесённых травм и общего состояния здоровья.");
        RESOURCE_TRANSLATIONS.put("health_join_now", "Присоединиться");
        RESOURCE_TRANSLATIONS.put("onboarding_welcome_use", "Добро пожаловать");
        RESOURCE_TRANSLATIONS.put("onboarding_slogan", "Здоровье в гармонии с жизнью");
        RESOURCE_TRANSLATIONS.put("onboarding_app_name", "Исследование здоровья Xiaomi");
        RESOURCE_TRANSLATIONS.put("onboarding_please_read", "Прочитайте и примите");
        RESOURCE_TRANSLATIONS.put("onboarding_disagree_and_continue", "Не соглашаться и перейти в базовый режим");
        RESOURCE_TRANSLATIONS.put("onboarding_privacy_tips_xieyi", " <a href=\"%1$s\">«Пользовательское соглашение Mi Health Research»</a>");
        RESOURCE_TRANSLATIONS.put("onboarding_privacy_tips_yinsi", " <a href=\"%1$s\">«Политика конфиденциальности Mi Health Research»</a>");
        RESOURCE_TRANSLATIONS.put("onboarding_privacy_tips_zhaiyao", " <a href=\"%1$s\">(краткое изложение политики конфиденциальности)</a>");
        RESOURCE_TRANSLATIONS.put("onboarding_privacy_tips_2", " <a href=\"%1$s\">«Пользовательское соглашение Mi Health Research»</a>, <a href=\"%2$s\">«Политика конфиденциальности Mi Health Research»</a><a href=\"%3$s\"> (краткое изложение)</a>");
        RESOURCE_TRANSLATIONS.put("onboarding_join_experience_program", " Присоединиться к <a href=\"%1$s\">программе улучшения пользовательского опыта</a> и помочь улучшить продукты и услуги.");
        RESOURCE_TRANSLATIONS.put("onboarding_read_and_agree_privacy", "Прочитайте и примите нашу <a href=\"%1$s\">Политику конфиденциальности</a>, чтобы узнать о ваших правах и обработке данных.");
        RESOURCE_TRANSLATIONS.put("agree", "Согласен");
        RESOURCE_TRANSLATIONS.put("cancel", "Отмена");
        RESOURCE_TRANSLATIONS.put("mine_user_agreement", "Пользовательское соглашение");
        RESOURCE_TRANSLATIONS.put("mine_user_privacy_policy", "Политика конфиденциальности");
        RESOURCE_TRANSLATIONS.put("mine_user_privacy_policy_summary", "Краткое изложение политики конфиденциальности");
        RESOURCE_TRANSLATIONS.put("mine_ser_experience_improvement_plan", "Программа улучшения пользовательского опыта");
        RESOURCE_TRANSLATIONS.put("mine_user_experience_improvement", "Участвовать в программе улучшения пользовательского опыта");
        RESOURCE_TRANSLATIONS.put("mine_user_experience_improvement_plan", "Программа улучшения пользовательского опыта");
        RESOURCE_TRANSLATIONS.put("mine_user_experience_improvement_tips", "Мы анализируем использование отдельных функций, чтобы улучшать продукты и услуги. Обработка данных осуществляется в соответствии с нашей политикой конфиденциальности.");
        RESOURCE_TRANSLATIONS.put("health_add_new_device", "Добавить новое устройство");
        RESOURCE_TRANSLATIONS.put("health_calendar_title", "История данных");
        RESOURCE_TRANSLATIONS.put("health_current", "Сегодня");
        RESOURCE_TRANSLATIONS.put("health_no_data", "Нет данных");
        RESOURCE_TRANSLATIONS.put("health_no_net", "Нет подключения к сети. Повторите попытку.");
        RESOURCE_TRANSLATIONS.put("health_research_history_record", "История");
        RESOURCE_TRANSLATIONS.put("health_research_latest_record", "Последний результат");
        RESOURCE_TRANSLATIONS.put("health_view_now", "Посмотреть");
        RESOURCE_TRANSLATIONS.put("health_sport_research_view_now", "Посмотреть");
        RESOURCE_TRANSLATIONS.put("health_sport_high_risk", "Высокий риск");
        RESOURCE_TRANSLATIONS.put("health_sport_mid_high_risk", "Повышенный риск");
        RESOURCE_TRANSLATIONS.put("health_sport_mid_risk", "Средний риск");
        RESOURCE_TRANSLATIONS.put("health_sport_low_risk", "Низкий риск");
        RESOURCE_TRANSLATIONS.put("health_sleep_high_risk", "Вероятно, высокий риск");
        RESOURCE_TRANSLATIONS.put("health_sleep_mid_risk", "Вероятно, средний риск");
        RESOURCE_TRANSLATIONS.put("health_sleep_low_risk", "Вероятно, низкий риск");
        RESOURCE_TRANSLATIONS.put("health_sleep_no_abnormality", "Отклонений не выявлено");
        RESOURCE_TRANSLATIONS.put("hospital_heart_name", "Исследование здоровья сердца");
        RESOURCE_TRANSLATIONS.put("hospital_bloodpressure_name", "Исследование артериального давления");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_apnea_research", "Исследование апноэ сна");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_apnea_health_research", "Исследование апноэ сна");
        RESOURCE_TRANSLATIONS.put("hospital_sport_research_join_now", "Присоединиться");
        RESOURCE_TRANSLATIONS.put("mine_privacy_policy_revoke_agreement", "Отозвать согласие с политикой конфиденциальности");
        RESOURCE_TRANSLATIONS.put("device_available_devices", "Устройства");
        RESOURCE_TRANSLATIONS.put("device_heart_research", "Исследование здоровья сердца");
        RESOURCE_TRANSLATIONS.put("device_sleep_apnea_research", "Исследование апноэ сна");
        RESOURCE_TRANSLATIONS.put("hospital_heart_research_join_now", "Присоединиться");
        RESOURCE_TRANSLATIONS.put("hospital_bloodpressure_available_devices", "Доступные устройства");
        RESOURCE_TRANSLATIONS.put("hospital_heart_available_devices", "Доступные устройства");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_available_devices", "Доступные устройства");
        RESOURCE_TRANSLATIONS.put("hospital_heart_research_agree", "Согласиться и продолжить");
        RESOURCE_TRANSLATIONS.put("hospital_heart_research_agree_clause", "Я внимательно прочитал(а) и согласен(на) с условиями выше");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_agree", "Согласен");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_agree_and_continue", "Согласиться и продолжить");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_agree_clause", "Я внимательно прочитал(а) и согласен(на) с условиями выше");
        RESOURCE_TRANSLATIONS.put("hospital_sport_research_agree", "Согласиться и продолжить");
        RESOURCE_TRANSLATIONS.put("hospital_sport_research_agree_clause", "Я внимательно прочитал(а) и согласен(на) с условиями выше");
        RESOURCE_TRANSLATIONS.put("hospital_heart_research_informed_consent", "Информированное согласие");
        RESOURCE_TRANSLATIONS.put("hospital_sleep_informed_consent", "Информированное согласие");
        RESOURCE_TRANSLATIONS.put("hospital_sport_research_informed_consent", "Информированное согласие");

        DYNAMIC_TEXT_TRANSLATIONS.put("小米健康研究", "Исследование здоровья Xiaomi");
        DYNAMIC_TEXT_TRANSLATIONS.put("畅享健康生活", "Здоровье в гармонии с жизнью");
        DYNAMIC_TEXT_TRANSLATIONS.put("健康", "Здоровье");
        DYNAMIC_TEXT_TRANSLATIONS.put("设备", "Устройства");
        DYNAMIC_TEXT_TRANSLATIONS.put("我的", "Профиль");
        DYNAMIC_TEXT_TRANSLATIONS.put("立即加入", "Присоединиться");
        DYNAMIC_TEXT_TRANSLATIONS.put("同意", "Согласен");
        DYNAMIC_TEXT_TRANSLATIONS.put("取消", "Отмена");
        DYNAMIC_TEXT_TRANSLATIONS.put("不同意并进入基础模式", "Не соглашаться и перейти в базовый режим");
        DYNAMIC_TEXT_TRANSLATIONS.put("心脏健康研究", "Исследование здоровья сердца");
        DYNAMIC_TEXT_TRANSLATIONS.put("血压健康研究", "Исследование артериального давления");
        DYNAMIC_TEXT_TRANSLATIONS.put("睡眠呼吸暂停研究", "Исследование апноэ сна");
        DYNAMIC_TEXT_TRANSLATIONS.put("跑步损伤评估", "Оценка риска беговых травм");
        DYNAMIC_TEXT_TRANSLATIONS.put("心律失常快速智能筛查，自主心脏健康管理。当出现心慌，心悸，胸闷，气短，乏力等不适症状时，请立即检测，及时识别风险，早日治疗。", "Быстрая интеллектуальная проверка на нарушения сердечного ритма и контроль здоровья сердца. При сердцебиении, перебоях в работе сердца, стеснении в груди, одышке, слабости и других тревожных симптомах немедленно пройдите проверку, чтобы своевременно выявить риск и обратиться за лечением.");
        DYNAMIC_TEXT_TRANSLATIONS.put("通过可穿戴设备，对心率、血氧饱和度和血压采集等多项健康指标进行监测，开展高血压智能筛查与预警、及血压管理研究。", "С помощью носимых устройств отслеживаются частота сердечных сокращений, насыщение крови кислородом, артериальное давление и другие показатели. Проводятся исследования для выявления риска гипертонии, предупреждения осложнений и контроля давления.");
        DYNAMIC_TEXT_TRANSLATIONS.put("通过可穿戴设备，对呼吸、心率、血氧饱和度和睡眠采集等多项健康指标进行监测，开展睡眠呼吸暂停的筛查与预警研究。", "С помощью носимых устройств отслеживаются дыхание, частота сердечных сокращений, насыщение крови кислородом, параметры сна и другие показатели для выявления риска апноэ сна и предупреждения о нём.");
        DYNAMIC_TEXT_TRANSLATIONS.put("基于您的跑步习惯、跑步后疼痛及恢复状况和个人身体健康状况等信息全面评估您的跑步损伤风险。", "Оценка риска беговых травм с учётом привычек бега, боли после пробежек, восстановления и общего состояния здоровья.");
        DYNAMIC_TEXT_TRANSLATIONS.put("小米健康研究用户体验改进计划", "Программа улучшения пользовательского опыта Mi Health Research");
        DYNAMIC_TEXT_TRANSLATIONS.put("小米健康研究用户协议", "Пользовательское соглашение Mi Health Research");
        DYNAMIC_TEXT_TRANSLATIONS.put("用户体验改进计划", "Программа улучшения пользовательского опыта");
    }

    @Override
    public void handleInitPackageResources(XC_InitPackageResources.InitPackageResourcesParam resparam) {
        if (!TARGET_PACKAGE.equals(resparam.packageName)) return;
        for (Map.Entry<String, String> entry : RESOURCE_TRANSLATIONS.entrySet()) {
            try {
                resparam.res.setReplacement(TARGET_PACKAGE, "string", entry.getKey(), entry.getValue());
            } catch (Throwable error) {
                XposedBridge.log("MiHealth RU: resource not replaced: " + entry.getKey() + " / " + error);
            }
        }
        XposedBridge.log("MiHealth RU: runtime resource replacements registered: " + RESOURCE_TRANSLATIONS.size());
    }

    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (!TARGET_PACKAGE.equals(lpparam.packageName)) return;
        hookTextView();
        hookWebViewLocale();
        XposedBridge.log("MiHealth RU: runtime hooks active for " + TARGET_PACKAGE);
    }

    private static void hookTextView() {
        XC_MethodHook textHook = new XC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam param) {
                Object arg = param.args[0];
                if (!(arg instanceof CharSequence)) return;
                String original = ((CharSequence) arg).toString();
                String translated = translateDynamicText(original);
                if (translated != null && !translated.equals(original)) param.args[0] = translated;
            }
        };
        try {
            XposedHelpers.findAndHookMethod(TextView.class, "setText", CharSequence.class, textHook);
        } catch (Throwable error) {
            XposedBridge.log("MiHealth RU: TextView.setText hook failed: " + error);
        }
        try {
            XposedHelpers.findAndHookMethod(TextView.class, "setText", CharSequence.class, TextView.BufferType.class, textHook);
        } catch (Throwable error) {
            XposedBridge.log("MiHealth RU: TextView.setText(BufferType) hook failed: " + error);
        }
    }

    private static String translateDynamicText(String text) {
        if (text == null) return null;
        String direct = DYNAMIC_TEXT_TRANSLATIONS.get(text);
        if (direct != null) return direct;
        String normalized = text.trim().replaceAll("\\s+", " ");
        direct = DYNAMIC_TEXT_TRANSLATIONS.get(normalized);
        return direct;
    }

    private static void hookWebViewLocale() {
        XC_MethodHook singleArgHook = new XC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam param) {
                if (!(param.args[0] instanceof String)) return;
                String original = (String) param.args[0];
                String changed = rewriteXiaomiLocaleUrl(original);
                if (!original.equals(changed)) {
                    param.args[0] = changed;
                    XposedBridge.log("MiHealth RU: WebView locale URL changed to " + changed);
                }
            }
        };
        try {
            XposedHelpers.findAndHookMethod(WebView.class, "loadUrl", String.class, singleArgHook);
        } catch (Throwable error) {
            XposedBridge.log("MiHealth RU: WebView.loadUrl hook failed: " + error);
        }
        try {
            XposedHelpers.findAndHookMethod(WebView.class, "loadUrl", String.class, Map.class, singleArgHook);
        } catch (Throwable error) {
            XposedBridge.log("MiHealth RU: WebView.loadUrl(headers) hook failed: " + error);
        }
    }

    private static String rewriteXiaomiLocaleUrl(String raw) {
        if (TextUtils.isEmpty(raw)) return raw;
        final Uri uri;
        try { uri = Uri.parse(raw); } catch (Throwable ignored) { return raw; }
        String host = uri.getHost();
        String path = uri.getPath();
        if (host == null || path == null || !"watch.iot.mi.com".equalsIgnoreCase(host)) return raw;
        boolean legalPage = path.startsWith("/html/privacy/index.html");
        boolean researchPage = path.startsWith("/html/general/index.html");
        if (!legalPage && !researchPage) return raw;

        String changed = raw.replace("locale=zh_cn", "locale=ru_ru")
                .replace("locale=zh-CN", "locale=ru_ru")
                .replace("lang=zh-CN", "lang=ru-RU")
                .replace("lang=zh_cn", "lang=ru-RU");

        // The privacy-page links in the original DEX omit a locale query. Ask the server
        // for Russian without touching route, type, fragment, cookies, or request body.
        if (legalPage && !changed.matches(".*[?&]locale=[^&#]+.*")) {
            int hash = changed.indexOf('#');
            String head = hash >= 0 ? changed.substring(0, hash) : changed;
            String fragment = hash >= 0 ? changed.substring(hash) : "";
            changed = head + (head.contains("?") ? "&" : "?") + "locale=ru_ru" + fragment;
        }
        return changed;
    }
}
