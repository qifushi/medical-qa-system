
export function useSSEWriter() {
    // 流式写入方法
    function writeStream({
        reader,
        onContent,
        onEnd,
        onError,
    }: {
        reader: ReadableStreamDefaultReader
        onContent: (content: string, chunk?: any) => void
        onEnd?: () => void
        onError?: (err: any) => void
    }) {
        let tempResult = ''
        const decoder = new TextDecoder('utf-8')

        const read = async () => {
            try {
                // eslint-disable-next-line no-constant-condition
                while (true) {
                    const { done, value } = await reader.read()
                    if (done) {
                        onEnd && onEnd()
                        break
                    }
                    const str = decoder.decode(value, { stream: true })
                    tempResult += str
                    // 匹配所有 data: {...}\n\n
                    const split = tempResult.match(/data:.*}\n\n/g)
                    if (split) {
                        for (const item of split) {
                            try {
                                const chunk = JSON.parse(item.replace('data:', ''))
                                if (chunk?.content) {
                                    onContent(chunk.content, chunk)
                                }
                                if (chunk?.is_end) {
                                    onEnd && onEnd()
                                    return
                                }
                            } catch (e) {
                                onError && onError(e)
                            }
                        }
                        tempResult = tempResult.replace(split.join(''), '')
                    }
                }
            } catch (err) {
                onError && onError(err)
            }
        }
        read()
    }
    // 一次性返回JSON
    function writeJson({
        reader,
        onContent,
        onEnd,
        onError,
    }: {
        reader: ReadableStreamDefaultReader
        onContent: (content: string, chunk?: any) => void
        onEnd?: () => void
        onError?: (err: any) => void
    }) {
        let tempResult = ''
        const decoder = new TextDecoder('utf-8')
        const read = async () => {
            try {
                // eslint-disable-next-line no-constant-condition
                while (true) {
                    const { done, value } = await reader.read()
                    if (done) {
                        try {
                            const result_block = JSON.parse(tempResult)
                            if (result_block.content) {
                                onContent(result_block.content, result_block)
                            }
                            onEnd && onEnd()
                        } catch (e) {
                            onError && onError(e)
                        }
                        break
                    }
                    if (value) {
                        tempResult += decoder.decode(value)
                    }
                }
            } catch (err) {
                onError && onError(err)
            }
        }
        read()
    }
    return {
        writeStream,
        writeJson
    }
}