renderMathquil = function(query, initMathQuill) {
    console.log(query)
    var MQ = MathQuill.getInterface(2);

    var composedKeys = {
        cos: ["cos", "(", ")", "left"],
        sin: ["sin", "(", ")", "left"],
        tan: ["tan", "(", ")", "left"],
        log: ["log", "(", ")", "left"],
        log_: ["log", "_", "right", "(", ")", "left", "left", "left"],
        ln: ["ln", "(", ")", "left"],
        "()": ["(", ")", "left"],
    }

    var specialKeys = {
        right: "Right",
        left: "Left",
        Down: "Down",
        Up: "Up",
        bksp: "Backspace",
        tab: "Tab"
    }

    // add special keys, but don't override previous keyaction definitions
    Object.keys(specialKeys).forEach(function(key){
        if (!$.keyboard.keyaction[key]) {
            $.keyboard.keyaction[key] = specialKeys[key];
        }
    });

    query.each(function(index, mq) {
        var mq_keyboard = initMathQuill(MQ, index, mq);
        var mathquill = mq_keyboard[0];
        var keyboard = mq_keyboard[1];

        $(mq).click(function(){
            // keyboard.getkeyboard().reveal();
            keyboard.getkeyboard().reveal();
        })

        keyboard
            .on('keyboardChange', function(e, keyboard, el) {
                console.log(e.action);
                if (specialKeys[e.action]) {
                    mathquill.keystroke(specialKeys[e.action]);
                } else if (composedKeys[e.action]) {
                    $(composedKeys[e.action]).each(function(index, value) {
                        if (specialKeys[value]) {
                            mathquill.keystroke(specialKeys[value]);
                        } else {
                            mathquill.cmd(value);
                        }
                    });
                } else {
                    mathquill.cmd(e.action);
                }
                // $('#mathquill').focus();
            })
        .keyboard({
            usePreview: false,
            lockInput: true,
            noFocus: true,
            layout: 'custom',
            display: {
                "Down": "&darr;",
                "Up": "&uarr;"
            },
            customLayout: MATH_CUSTOM_LAYOUT[$(mq).attr("data-keyboard-type")],
            useCombos: false
        })
        // activate the typing extension
        .addTyping({
            showTyping: true,
            delay: 250
        });
    });
};
