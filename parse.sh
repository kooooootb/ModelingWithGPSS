#!/bin/bash

function get_average () {
	sum=0
	n=0
	while(( $# ))
	do
		sum=$(echo "$1 + $sum" | bc)
		n=$((n + 1))
		shift
	done
	echo "scale=3;$sum / $n" | bc -l
}

# Базовое название файла
fn='init0.gpr'

# Файл вывода
foutput='python/config.py'

# Массивы значений очередей на блоки
qpreprocArr=()
qassemblyArr=()
qadjustArr=()

# Массивы значений загрузок блоков
ppreprocArr=()
passemblyArr=()
padjustArr=()

# Массив оптимизируемых параметров
parametersArr=()

# Обработка файлов
for currentfn in ./*.gpr
do
	# Заполнение массивов очередей
	lines="$(cat $currentfn | grep --text -A 3 ^QUEUE | tail -3)"
	{ read linePreproc; read lineAssembly; read lineAdjust; } <<< "$lines"
	qpreproc="$(read -r line <<< "$linePreproc"; echo $line | awk '{print $6}')"; qpreprocArr+=($qpreproc)
	qassembly="$(read -r line <<< "$lineAssembly"; echo $line | awk '{print $6}')"; qassemblyArr+=($qassembly)
	qadjust="$(read -r line <<< "$lineAdjust"; echo $line | awk '{print $6}')"; qadjustArr+=($qadjust)

	# Заполнение массивов загрузок
	lines="$(cat $currentfn | grep --text -A 3 ^FACILITY | tail -3)"
	{ read linePreproc; read lineAssembly; read lineAdjust; } <<< "$lines"
	ppreproc="$(read -r line <<< "$linePreproc"; echo $line | awk '{print $3}')"; ppreprocArr+=($ppreproc)
	passembly="$(read -r line <<< "$lineAssembly"; echo $line | awk '{print $3}')"; passemblyArr+=($passembly)
	padjust="$(read -r line <<< "$lineAdjust"; echo $line | awk '{print $3}')"; padjustArr+=($padjust)

	# Заполнение массива параметров
	parametersArr+=("$(cat $currentfn | grep --text -A 100 ^SAVEVALUE | sed -n '/^SAVEVALUE/,$p' | grep --text '^ PARAMETER' | awk '{print $3}')")
done

# Сброс выводного файла
echo 'import numpy as np' > $foutput

# Вывод очередей
printf -v joined '%s,' "${qpreprocArr[@]}"; echo -e "preproc_queue = np.array([${joined%,}])" >> $foutput
printf -v joined '%s,' "${qassemblyArr[@]}"; echo -e "assembly_queue = np.array([${joined%,}])" >> $foutput
printf -v joined '%s,' "${qadjustArr[@]}"; echo -e "adjust_queue = np.array([${joined%,}])" >> $foutput

# Вывод загрузок
printf -v joined '%s,' "${ppreprocArr[@]}"; echo -e "preproc_utility = np.array([${joined%,}])" >> $foutput
printf -v joined '%s,' "${passemblyArr[@]}"; echo -e "assembly_utility = np.array([${joined%,}])" >> $foutput
printf -v joined '%s,' "${padjustArr[@]}"; echo -e "adjust_utility = np.array([${joined%,}])" >> $foutput

# Вывод параметров
printf -v joined '%s,' "${parametersArr[@]}"; echo -e "parameters = np.array([${joined%,}])" >> $foutput

