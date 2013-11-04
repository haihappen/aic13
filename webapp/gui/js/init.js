
Ext.onReady(function () {
    Ext.QuickTips.init();
	
	createViewport(getGrid());

	/*Ext.Ajax.request({
		url:'/user',
		method:"GET",
		success:function (response) {
			var user = Ext.decode(response.responseText);
			createViewport(user);
			autostart();
		}
	});*/
});

function createViewport(items) {
    Ext.create('Ext.container.Viewport', {
        layout: 'border',
        items: items
    });
}


function getGrid() {
	Ext.create('Ext.data.Store', {
		storeId:'taskStore',
		fields:['TaskDescription', 'AnswerPossibilities', 'CallbackLink', 'Price'],
		data: { 'items' : data },
		proxy: {
			type: 'memory',
			reader: {
				type: 'json',
				root: 'items'
			}
		}
	});

	var grid = Ext.create('Ext.grid.Panel', {
		title: 'Tasklist',
		store: Ext.data.StoreManager.lookup('taskStore'),
		region: "center",
		columns: [
			{ text: 'TaskDescription',  dataIndex: 'TaskDescription', flex: 1},
			{ text: 'Price', dataIndex: 'Price'},
			{
				xtype:'actioncolumn',
				width:25,
				items: [{
					icon: 'style/icons/answer.png',  // Use a URL in the icon config
					tooltip: 'rate this text',
					handler: function(grid, rowIndex, colIndex) {
						var rec = grid.getStore().getAt(rowIndex);
						showWindow(rec);
					}
				}]
			}
		],
		listeners : {
			'itemdblclick' : function(t, record, item, index, e, eOpts ){
				showWindow(record);
			}
		}
	});
	return grid;
}

function showWindow(rec){
	var win = Ext.create('Ext.window.Window', {
		title: 'Please rate the following text',
		id: "taskWindow",
		width: 400,
		height: 300,
		layout: 'fit',
		resizable: false,
		modal: true,
		frame: true,
		items: {
			xtype: 'panel',
			layout: 'border',
			items : [{
				xtype: 'panel',
				region: 'center',
				layout: 'fit',
				items: getTextArea(rec.get('TaskDescription'))
			},{
				xtype: 'panel',
				region: 'south',
				items : getForm(rec)
			}]
		},
		buttons : [
			{
				xtype: 'button',
				text : 'Submit',
				listeners: {
					click: function() {
						if(Ext.getCmp('form').isValid()){
							alert("do request");
							Ext.getCmp("taskWindow").destroy();
						}else{
							Ext.MessageBox.show({
							   title: 'Error',
							   msg: 'Please enter a userID and choose an answer',
							   buttons: Ext.MessageBox.OK,
							   icon: Ext.MessageBox.WARNING
						   });
						}
					}		
				},
				width: "100%"
			}
		]
	});
	
	win.show();
}

function getForm(rec){
	return {
		xtype: 'form',
		frame: true,
		id: 'form',
		items : [
			{
				xtype: 'textfield',
				name: 'user',
				labelWidth: 50,
				fieldLabel: "UserID",
				width: 373,
				id: 'userId',
				allowBlank: false
			},
			{
				fieldLabel: "Choose an anwer",
				xtype: 'combo',
				store: rec.get("AnswerPossibilities"),
				width: 373,
				id: 'answers',
				allowBlank: false
			}
		]
	};
}

function getTextArea(text){
	return{
		xtype: 'textarea',
		name: 'TaskDescription',
		width: "100%",
		readOnly: true,
		height: "auto",
		value: text
	};
}