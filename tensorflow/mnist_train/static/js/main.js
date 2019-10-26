document.write("<script language=javascript src='http://echarts.baidu.com/build/dist/echarts.js'></script>");
class Main {
    constructor() {
        this.canvas = document.getElementById('main');
        this.input = document.getElementById('input');
        this.canvas.width = 449; // 16 * 28 + 1
        this.canvas.height = 449; // 16 * 28 + 1
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.initialize();
    }

    initialize() {
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.fillRect(0, 0, 449, 449);
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(0, 0, 449, 449);
        this.ctx.lineWidth = 0.05;
        for (var i = 0; i < 27; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo((i + 1) * 16, 0);
            this.ctx.lineTo((i + 1) * 16, 449);
            this.ctx.closePath();
            this.ctx.stroke();

            this.ctx.beginPath();
            this.ctx.moveTo(0, (i + 1) * 16);
            this.ctx.lineTo(449, (i + 1) * 16);
            this.ctx.closePath();
            this.ctx.stroke();
        }
        this.drawInput();
        $('#output td').text('').removeClass('success');
    }

    onMouseDown(e) {
        this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.getPosition(e.clientX, e.clientY);
    }

    onMouseUp() {
        this.drawing = false;
        this.drawInput();
    }

    onMouseMove(e) {
        if (this.drawing) {
            var curr = this.getPosition(e.clientX, e.clientY);
            this.ctx.lineWidth = 16;
            this.ctx.lineCap = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(this.prev.x, this.prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            this.ctx.closePath();
            this.prev = curr;
        }
    }

    getPosition(clientX, clientY) {
        var rect = this.canvas.getBoundingClientRect();
        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    drawInput() {
        var ctx = this.input.getContext('2d');
        var img = new Image();
        img.onload = () => {
            var inputs = [];
            var small = document.createElement('canvas').getContext('2d');
            small.drawImage(img, 0, 0, img.width, img.height, 0, 0, 28, 28);
            var data = small.getImageData(0, 0, 28, 28).data;
            for (var i = 0; i < 28; i++) {
                for (var j = 0; j < 28; j++) {
                    var n = 4 * (i * 28 + j);
                    inputs[i * 28 + j] = (data[n + 0] + data[n + 1] + data[n + 2]) / 3;
                    ctx.fillStyle = 'rgb(' + [data[n + 0], data[n + 1], data[n + 2]].join(',') + ')';
                    ctx.fillRect(j * 5, i * 5, 5, 5);
                }
            }
            if (Math.min(...inputs) === 255) {
                return;
            }
            $.ajax({
                url: '/api/mnist',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(inputs),
                success: (data) => {
                    data = JSON.parse(data);
                    var value_1=new Array();
                    var value_2 = new Array();
                    var sum_1 = 0;
                    var sum_2 = 0
                    for(var i=0;i<(data["site"][0]["output1"]).length;i++)
                    {
                        if (Math.round(data["site"][0]["output1"][i] * 100) > 0){
                            value_1[i] = Math.round(data["site"][0]["output1"][i] * 100);
                            sum_1 += Math.round(data["site"][0]["output1"][i] * 100)
                        }else{
                            value_1[i] = 0
                        }
                    }
                    for(var i=0;i<(data["site"][0]["output2"]).length;i++)
                    {
                        if (Math.round(data["site"][0]["output2"][i] * 100) > 0){
                            value_2[i] = Math.round(data["site"][0]["output2"][i] * 100);
                            sum_2 += Math.round(data["site"][0]["output2"][i] * 100)
                        }else{
                            value_2[i] = 0
                        }
                    }
                    // 获取最大值

                    var max_1 = Math.max.apply(Math,value_1);
                    var max_2 = Math.max.apply(Math,value_2);
                    var max_index_1 = value_1.indexOf(max_1);
                    var max_index_2 = value_2.indexOf(max_2);
                    for (let j=0;j<10;j++)
                    {
                         $('#result tr').eq(j + 1).find('td').eq(1).text(value_1[j] / sum_1 * 100 + "%");
                         if(j===max_index_1){
                             $('#result tr').eq(max_index_1+1).find('td').eq(1).addClass('success');
                         }
                    }
                    for (let j=0;j<10;j++)
                    {
                         $('#result tr').eq(j + 1).find('td').eq(2).text(value_2[j] / sum_2 *100 + "%");
                         if(j===max_index_1){
                             $('#result tr').eq(max_index_2+1).find('td').eq(2).addClass('success');
                         }
                    }

                }
            });
        };
        img.src = this.canvas.toDataURL();
    }
}

$(() => {
    var main = new Main();
    $('#clear').click(() => {
        main.initialize();
        console.log("hahh");
        for(let i=0;i<2;i++)
        {
            for(j=0;j<10;j++)
            {
                $('#result tr').eq(j + 1).find('td').eq(i+1).text(" ");
                $('#result tr').eq(j + 1).find('td').eq(i+1).removeClass('success');
            }
        }
    });
});